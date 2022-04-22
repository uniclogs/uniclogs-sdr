#!/bin/bash

# get current user and group for -u arg
USER_AND_GROUP=$(id -u ${USER}):$(id -g ${USER})

# make these if they don't exist
mkdir -p ~/.gnuradio
mkdir -p ~/.cache/grc_gnuradio
mkdir -p ~/.cache/matplotlib
mkdir -p ~/.config/matplotlib
touch ~/.gr_fftw_wisdom.lock

docker run \
    --rm \
    -w /flowgraphs \
    -u $USER_AND_GROUP \
    -e XAUTHORITY=/tmp/xauth \
    -v ~/.Xauthority:/tmp/xauth \
    -v /tmp/.X11-unix/:/tmp/ \
    -v `pwd`/flowgraphs:/flowgraphs \
    -v ~/.gnuradio:/.gnuradio \
    -v ~/.cache/grc_gnuradio:/.cache/grc_gnuradio \
    -v ~/.cache/matplotlib:/.cache/matplotlib \
    -v ~/.config/matplotlib:/.config/matplotlib \
    -v ~/.gr_fftw_wisdom.lock:/.gr_fftw_wisdom.lock \
    -e DISPLAY=:0 \
    --net host \
    oresat/uniclogs-sdr-base:gr-39
