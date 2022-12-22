#!/bin/bash
tc qdisc add dev vboxnet1 root netem delay 10ms
tc qdisc show