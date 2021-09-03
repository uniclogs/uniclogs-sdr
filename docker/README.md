# UniClOGS SDR GNURadio Docker and Makefile

This folder contains content to run gnuradio in a docker container

## Prerequisites

* make
* docker
* docker-compose

## Builing, running, and simulating data in GNURadio

Here are some commands to get things started:

To list available make targets:

    make

To run the all target:

    make all

To build gnuradio:

    make build

To bring up gnuradio container:

    make up

To bring down gnuradio container:

    make down

To shell into gnuradio container:

    make shell
