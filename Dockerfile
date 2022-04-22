FROM debian:bullseye

# install dependencies
# Note: the libuhd recommends gnuradio 3.8 package annoyingly
RUN apt-get update && apt-get -y --no-install-recommends install \
    bzip2 \
    cmake \
    g++ \
    gir1.2-gtk-3.0 \
    git \
    gsl-bin \
    gpredict \
    libasound2 \
    libblas-dev \
    libboost-all-dev \
    libcppunit-dev \
    libcodec2-dev \
    libfftw3-dev \
    libglu1-mesa \
    libgmp3-dev \
    libgslcblas0 \
    libgtk-3-dev \
    libjack-jackd2-0 \
    liblimesuite-dev \
    liblog4cpp5-dev \
    liborc-dev \
    libportaudiocpp0 \
    libsndfile1-dev \
    libqwt-qt5-6 \
    libqwt-qt5-dev \
    libqt5svg5-dev \
    libsoapysdr-dev \
    libuhd-dev  \
    libusb-1.0-0 \
    libvolk2-dev \
    libzmq3-dev \
    limesuite \
    ninja-build \
    pybind11-dev \
    python3 \
    python3-cheetah \
    python3-click \
    python3-click-plugins \
    python3-construct \
    python3-gi \
    python3-gi-cairo \
    python3-jsonschema \
    python3-mako \
    python3-matplotlib \
    python3-numpy \
    python3-pygccxml \
    python3-pyqt5 \
    python3-pyqtgraph \
    python3-scipy \
    python3-sphinx \
    python3-yaml \
    python3-zmq \
    qtbase5-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# fix the python path
ENV PYTHONPATH "{PYTHONPATH}:/usr/lib/python3.9/site-packages"

# download last gnuradio 3.9 release
RUN wget https://github.com/gnuradio/gnuradio/archive/refs/tags/v3.9.6.0.tar.gz && \
    tar xvf v3.9.6.0.tar.gz && \
    cd gnuradio-3.9.6.0 && \
    mkdir build && \
    cd build && \
    cmake \
        -DENABLE_GRC=ON \
        -DENABLE_GR_QTGUI=ON \
        -DENABLE_GR_CTRLPORT=OFF \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DGR_PYTHON_DIR=/usr/lib/python3.9/site-packages \
        -DQWT_LIBRARIES=/usr/lib/libqwt-qt5.so \
        -Wno-dev \
        -GNinja \
        .. && \
    ninja && \
    ninja install && \
    ldconfig && \
    cd / && \
    rm -rf *.tar.gz gnuradio-*

# build and install latest gr-satellites module
RUN wget https://github.com/daniestevez/gr-satellites/archive/refs/tags/v4.5.0.tar.gz && \
    tar xvf v4.5.0.tar.gz && \
    mkdir -p gr-satellites-4.5.0/build && \
    cd gr-satellites-4.5.0/build && \
    cmake \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DCMAKE_BUILD_TYPE=Release \
        -GNinja \
        .. && \
    ninja && \
    ninja install && \
    ldconfig && \
    cd / && \
    rm -rf *.tar.gz gr-satellites-*

# build and install gr-limesdrA module
RUN git clone https://github.com/daniestevez/gr-limesdr && \
    mkdir -p gr-limesdr/build && \
    cd gr-limesdr/build && \
    git checkout gr39 && \
    cmake \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DCMAKE_BUILD_TYPE=Release \
        -GNinja \
        .. && \
    ninja && \
    ninja install && \
    ldconfig && \
    cd / && \
    rm -rf gr-limesdr

# build and install gr-gpredict-doppler module
RUN git clone https://github.com/ghostop14/gr-gpredict-doppler && \
    mkdir -p gr-gpredict-doppler/build && \
    cd gr-gpredict-doppler/build && \
    cmake \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DCMAKE_BUILD_TYPE=Release \
        -GNinja \
        .. && \
    ninja && \
    ninja install && \
    ldconfig && \
    cd / && \
    rm -rf gr-gpredict-doppler

CMD ["gnuradio-companion"]
