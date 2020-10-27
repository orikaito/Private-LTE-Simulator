FROM ubuntu:18.04
RUN sed -i.bak -e "s%http://[^ ]\+%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list
RUN apt-get update \
    && apt-get -y install \
    iputils-ping \
    net-tools \
    iproute2