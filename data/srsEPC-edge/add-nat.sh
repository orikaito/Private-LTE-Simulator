#!/bin/bash
iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -d 192.168.32.0/24 -o enp0s9 -j MASQUERADE