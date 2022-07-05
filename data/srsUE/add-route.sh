#!/bin/bash
ip netns exec ue-career ip route add default via 172.16.0.1
ip netns exec ue-career iptables -t nat -A POSTROUTING -s 10.10.2.0/24 -d 192.168.30.0/24 -o tun_srsue -j MASQUERADE
ip netns exec ue-edge ip route add default via 172.16.0.1
ip netns exec ue-edge iptables -t nat -A POSTROUTING -s 10.12.2.0/24 -d 192.168.32.0/24 -o tun_srsue -j MASQUERADE