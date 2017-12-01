#!/usr/bin/env bash

REPLICA=$1
LAMBDA=$2


aprun -n 1 -N 1 -d 31 /u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2 +ppn 30 +pemap 0-29 +commap 30 replica_${REPLICA}/lambda_${LAMBDA}/min.conf >& replica_${REPLICA}/lambda_${LAMBDA}/min.log


aprun -n 1 -N 1 -d 31 /u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2 +ppn 30 +pemap 0-29 +commap 30 replica_${REPLICA}/lambda_${LAMBDA}/eq1.conf >& replica_${REPLICA}/lambda_${LAMBDA}/eq1.log


aprun -n 1 -N 1 -d 31 /u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2 +ppn 30 +pemap 0-29 +commap 30 replica_${REPLICA}/lambda_${LAMBDA}/eq2.conf >& replica_${REPLICA}/lambda_${LAMBDA}/eq2.log


aprun -n 1 -N 1 -d 31 /u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2 +ppn 30 +pemap 0-29 +commap 30 replica_${REPLICA}/lambda_${LAMBDA}/prod.conf >& replica_${REPLICA}/lambda_${LAMBDA}/prod.log

