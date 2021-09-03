FROM debian:bullseye

WORKDIR /uniclogs-sdr

# Install GNU Radio packages
RUN apt-get -q update && apt-get -qy install \
    gnuradio \
    gr-limesdr \
    gr-satellites
