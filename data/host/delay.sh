#!/bin/bash
tc qdisc add dev vboxnet1 root handle 1:0 netem delay 50ms