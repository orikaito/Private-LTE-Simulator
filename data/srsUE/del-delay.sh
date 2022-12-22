#!/bin/bash
tc qdisc del dev enx000ec6fb06a3 root netem delay 10ms
tc qdisc show