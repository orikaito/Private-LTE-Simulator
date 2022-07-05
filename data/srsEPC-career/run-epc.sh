#!/bin/bash
HOME_PATH=/home/srslte/
SRSEPC_PATH=srsRAN/build/
DATA_PATH=data/
"${HOME_PATH}${SRSEPC_PATH}srsepc/src/srsepc" "${HOME_PATH}${DATA_PATH}epc.conf"