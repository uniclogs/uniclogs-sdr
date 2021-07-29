#!/bin/bash
#
#  send_ax25_packet.sh
#
#  G.N. LeBrasseur
#  27-Jul-2021
#
#  Send a simple AX.25 packet to gr.
#
#  Source:         KJ7SU    SSID: 0
#  Destination:    SAT      SSID: 0
#  PID:            0x00
#  Control:        0x03
#  Payload:        Hi
#
echo "a682a84040406096946ea6aa406103004869" | xxd -r -p | nc localhost 52002
