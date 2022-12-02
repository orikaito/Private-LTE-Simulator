FROM ubuntu:18.04

EXPOSE 53
EXPOSE 53/udp

RUN apt-get update && \
    apt-get install iproute2 -y

ENTRYPOINT ["/etc/coredns/coredns"]
CMD ["-conf", "/etc/coredns/Corefile"]