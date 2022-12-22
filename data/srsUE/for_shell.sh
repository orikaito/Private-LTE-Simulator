#!/bin/bash
for i in `seq 1 100`
do
    echo "-------------- $i ---------------" && $1 && sleep 0.5;
done