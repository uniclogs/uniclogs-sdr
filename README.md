# uniclogs-sdr

[![License](https://img.shields.io/github/license/oresat/uniclogs-sdr)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/oresat/uniclogs-sdr)](https://github.com/oresat/uniclogs-sdr/issues)

GNURadio-based SDR software and flowgraphs for UniClOGS

# Distros Supported

* Debian Bullseye (just released 2021-07) "just works"
* Ubuntu 20.2 LTS but might need more work

# Packages you'll neeed!

* Python 3
* gnuradio 3.8 (NOT!! 3.9)
* gr-satellites 3.5
* gr-limesdr 3.0
* limesuite 20.10

# Setup

* Test the Lime Driver
   * Run `'LimeQuickTest`
   * Should be no errors
* Test your LimeMini
   * Run `LimeSuiteGUI`
   * Options > Connection Settings 
   * You should see your LimeSDR Mini -- double check the SN.
   * Choose it and click connect.
   * Click "Read Temp" in the upper right coerner and "Temperature:" Should swithc form ??? to a temp around 40 ish C.
   * Options > Connection Settings > Disconnect 
   * Quit!
* Load the INI file into the Lime RFE
   * Run `LimeSuiteGUI`
   * Modules > Lime RFE
   * Choose "Direct (USB)"
   * Choose Port > Open
   * Choose Configuration > Open  and chose the uniclogs-sdr/lime-rfe-setup.ini file
   * Quit!
* Run `gnuradio-companion`
   * In the GUI, on the lower right side, you should see "satellites" and "LimeSDR"
   * File > Open  and open `uniclogs-sdr/flowgraphs/lime_g3ruh.grc`
   * You might a concerning x-term error; just ignore it.
   * You should see the RF frequency sink (spectrograph).
   * If there's a beaconing C3 around, you should see data pop up on the left hand column! You might have to adjust the gain.

# Listening with YAMCS

* In the `uniclogs-yamcs` repo, you'll have to build and run yams (see the README.md file)
* Set up the Socket PDU to be: UDP Client, Host 127.0.0.1, Port 10015, MTU 10000.

# Transmitting

* You have to netcat to port 52002 the command you want to send. For example:
   * Turn on the battery: echo "C4F53800000F00E5111801" | xxd -r -p | nc -u 127.0.0.1 52002
   * Turn off the battery: echo "C4F53800000F00E5111800" | xxd -r -p | nc -u 127.0.0.1 52002 
