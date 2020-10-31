FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]
WORKDIR /workdir
RUN sed -i.bak -e "s%http://[^ ]\+%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list
RUN apt-get update \
    && apt-get -y install \
    iproute2 \
    iputils-ping \
    sudo \
    git \
    nano \
    cmake \
    libfftw3-dev \
    libmbedtls-dev \
    libboost-program-options-dev \
    libconfig++-dev \
    libsctp-dev
RUN git clone https://github.com/srsLTE/srsLTE.git \
    && cd srsLTE \
    && mkdir build \
    && cd build \
    && cmake ../ \
    && make \
    && make install \
    && ./srslte_install_configs.sh user