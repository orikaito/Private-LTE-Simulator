#!/bin/bash
SRSEPC_PATH=/Documents/srsRAN_edge/build
DATA_PATH=/Documents/Private-LTE-Simulator/data/srsUE
"${HOME}${SRSEPC_PATH}/srsenb/src/srsenb" "${HOME}${DATA_PATH}/enb-edge.conf"