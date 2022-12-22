#!/bin/bash
tc qdisc del dev vboxnet1 root netem delay 10ms
tc qdisc show