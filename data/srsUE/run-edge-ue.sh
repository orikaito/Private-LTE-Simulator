#!/bin/bash
HOME_PATH=/home/srslte/
SRSEPC_PATH=srsRAN-edge/build/
DATA_PATH=data/
"${HOME_PATH}${SRSEPC_PATH}srsue/src/srsue" "${HOME_PATH}${DATA_PATH}ue-edge.conf"