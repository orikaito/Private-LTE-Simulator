#!/bin/bash
tc qdisc add dev enx000ec6fb06a3 root netem delay 10ms
tc qdisc show