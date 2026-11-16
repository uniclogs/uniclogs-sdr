import sys, signal, pmt, time, threading
from PyQt5 import Qt
from gnuradio import uhd, gr, iio, network, pdu, blocks, filter, digital
from gnuradio.filter import firdes
from gnuradio.fft import window
import gnuradio.uniclogs as uniclogs
import numpy as np
from argparse import ArgumentParser

# rx

rx_samp_rate = 2e9
rx_symb_rate = 50e3
rx_bit_rate = 50e3
rx_gain = 35

SFD0 = [0x90, 0x4E]
SFD1 = [0x6F, 0x4E]  # used with FEC
preamble = [0b0101_0101] * 8

rx_target_freq = int(436.5e6)
lo_offset = int(500e3)
f_offset = int(500e3)
rx_tune_freq = rx_target_freq + lo_offset

device_serial = "3490D12"
sample_decimation_rate = 10
beacon_host = "localhost"
edl_host = "localhost"
# tx
tx_bt = 0.5
tx_samp_rate = int(2e6)
tx_bit_rate = 50000
tx_center_frequency = int(1265e6)
num_tones = 2
tx_symb_rate = tx_bit_rate * (num_tones / 2)
deviation = 50000
tx_gain = 85

tx_debug = True
rx_debug = True

class OreSat1(gr.top_block):
    def __init__(self, conf="OreSat1.cfg", tx_gain=30, txband="tx_l"):
        gr.top_block.__init__(
            self,
            "UHF G3RUH & EDL Receiver / UHF -or- L-Band EDL Transmitter",
            catch_exceptions=False,
        )
        self.flowgraph_started = threading.Event()

        # TX
        self.tx_socket = network.socket_pdu("UDP_SERVER", "", "10025", 10000, False)

        self.crc_append = digital.crc_append(
            32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, 0
        )

        # incoming packet -> crc_append
        self.msg_connect((self.tx_socket, "pdus"), (self.crc_append, "in"))

        self.ieee_encoder = uniclogs.ieee802_15_4_encoder(0x55, 8, SFD0, 69)
        self.frame_encoder = uniclogs.frame_encoder(self.ieee_encoder)

        # crc_append -> frame_encoder
        self.msg_connect((self.crc_append, "out"), (self.frame_encoder, "pdu"))

        self.pdu_to_tstream = pdu.pdu_to_tagged_stream(gr.types.byte_t, "packet_len")

        # frame_encoder -> pdu to tagged stream
        self.msg_connect((self.frame_encoder, "pdu"), (self.pdu_to_tstream, "pdus"))

        # frame_encoder -> edl_tx_note -> edl_tx_debug
        if (tx_debug):
            self.edl_tx_note = pdu.pdu_set(pmt.intern("note"), pmt.intern("EDL SENT"))
            self.edl_tx_debug = blocks.message_debug(True, gr.log_levels.info)

            self.msg_connect((self.frame_encoder, 'pdu'), (self.edl_tx_note, 'pdus'))
            self.msg_connect((self.edl_tx_note, 'pdus'), (self.edl_tx_debug, 'print'))

        self.gfsk_mod = digital.gfsk_mod(
            samples_per_symbol=(int(tx_samp_rate / tx_symb_rate)),
            sensitivity=((2 * np.pi * deviation) / tx_samp_rate),
            bt=tx_bt,
            verbose=False,
            log=False,
            do_unpack=True,
        )

        # pdu to tagged stream -> gfsk mod
        self.connect((self.pdu_to_tstream, 0), (self.gfsk_mod, 0))

        # self.tx_freqshift =
        # self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*0/self.tx_samp_rate)

        self.tx_sdr = iio.fmcomms2_sink_fc32(
            "ip:192.168.2.1" if "ip:192.168.2.1" else iio.get_pluto_uri(),
            [True, True],
            100000,
            False,
        )

        self.tx_sdr.set_frequency(tx_center_frequency)
        self.tx_sdr.set_bandwidth(tx_samp_rate)
        self.tx_sdr.set_samplerate(tx_samp_rate)
        self.tx_sdr.set_attenuation(0, 0)
        self.tx_sdr.set_filter_params("Auto", "", 0, 0)
        #self.tx_sdr.set_len_tag_key("packet_len")

        # gfsk_mod -> tx_sdr (pluto)
        self.connect((self.gfsk_mod, 0), (self.tx_sdr, 0))

        # RX
        self.rx_sdr = uhd.usrp_source(
            ",".join(("serial=" + device_serial, "")),
            uhd.stream_args(
                cpu_format="fc32",
                args="",
                channels=list(range(0, 1)),
            ),
        )

        self.rx_sdr.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.rx_sdr.set_antenna("RX2", 0)
        self.rx_sdr.set_gain(rx_gain, 0)
        self.rx_sdr.set_lo_source("internal", uhd.ALL_LOS, 0)
        self.rx_sdr.set_lo_export_enabled(False, uhd.ALL_LOS, 0)
        self.rx_freqshift = blocks.rotator_cc(2.0 * np.pi * (-f_offset) / rx_samp_rate)

        # rx_sdr -> freq_shift (for LO offset)
        self.connect((self.rx_sdr, 0), (self.rx_freqshift, 0))

        self.lowpass_filter = filter.fir_filter_ccf(
            sample_decimation_rate,
            firdes.low_pass(
                1,
                rx_samp_rate,
                (rx_symb_rate * 1.5),
                (rx_symb_rate * 0.75),
                window.WIN_HAMMING,
                6.76,
            ),
        )

        # freq_shift -> lowpass filter
        self.connect((self.rx_freqshift, 0), (self.lowpass_filter, 0))

        self.gfsk_demod = digital.gfsk_demod(
            samples_per_symbol=4,
            sensitivity=(rx_samp_rate / (2 * np.pi * rx_symb_rate)),
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.0002,
            freq_error=0.0,
            verbose=False,
            log=False,
        )

        # lowpass -> gfsk_demod
        self.connect((self.lowpass_filter, 0), (self.gfsk_demod, 0))

        self.ieee_decoder = uniclogs.ieee802_15_4_variant_decoder(preamble, 5, SFD0, 1)
        self.frame_decoder = uniclogs.frame_decoder(self.ieee_decoder, 1 * 1)

        # gfsk_demod -> frame_decoder
        self.connect((self.gfsk_demod, 0), (self.frame_decoder, 0))

        self.rx_socket = network.socket_pdu(
            "UDP_CLIENT", beacon_host, "10015", 10000, False
        )

        # debug info
        self.pdu_edl_note = pdu.pdu_set(pmt.intern("note"), pmt.intern("EDL RECIEVED"))
        self.edl_debug_msg = blocks.message_debug(True, gr.log_levels.info)

        # frame decoder -> rx_socket
        self.msg_connect((self.frame_decoder, "out"), (self.rx_socket, "pdus"))

        # frame decoder -> pdu_edl_note -> edl_debug_msg
        self.msg_connect((self.frame_decoder, "out"), (self.pdu_edl_note, "pdus"))
        self.msg_connect((self.pdu_edl_note, "pdus"), (self.edl_debug_msg, "print"))


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--conf",
        dest="conf",
        type=str,
        default="OreSat1.cfg",
        help="Set config file [default=%(default)r]",
    )
    parser.add_argument(
        "-t",
        "--tx-gain",
        dest="tx_gain",
        type=int,
        default=85,
        help="Set tx_gain [default=%(default)r]",
    )
    parser.add_argument(
        "-b",
        "--txband",
        dest="txband",
        type=str,
        default="tx_l",
        help="Set txband [default=%(default)r]",
    )
    return parser


def main(top_block_cls=OreSat1, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(
        conf=options.conf, tx_gain=options.tx_gain, txband=options.txband
    )

    tb.start()
    tb.flowgraph_started.set()

    # tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()


if __name__ == "__main__":
    main()
