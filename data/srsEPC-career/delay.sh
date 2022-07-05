#!/bin/bash
tc qdisc add dev enp0s9 root handle 1:0 netem delay 50ms