FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workdir
RUN sed -i.bak -e "s%http://[^ ]\+%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list
RUN apt-get update \
    && apt-get -y install \
    iproute2 \
    iputils-ping \
    sudo \
    git \
    nano \
    xxd
RUN git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git
RUN cd openairinterface5g/ \
    && git checkout -b v1.2.2 refs/tags/v1.2.2 \
    && source oaienv