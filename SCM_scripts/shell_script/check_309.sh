#!/bin/bash
for i in `seq 1 3600`
do
    ssh -p 29418 10.0.30.9 gerrit show-connections
    ssh -p 29418 10.0.30.9 gerrit show-queue
    date
    sleep  ${1}s
done
