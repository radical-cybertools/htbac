#!/bin/bash 
#PBS -A chm126
#PBS -N test
#PBS -q debug
#PBS -j oe
#PBS -l walltime=0:20:00
#PBS -l nodes=2

module load namd/2.12

export MPICH_PTL_SEND_CREDITS=-1
export MPICH_MAX_SHORT_MSG_SIZE=8000
export MPICH_PTL_UNEX_EVENTS=80000
export MPICH_UNEX_BUFFER_SIZE=100M

cd $MEMBERWORK/chm126/namd-bash

aprun -n 1 -N 1 -d 8 namd2 ++ppn 7 +setcpuaffinity +pemap 0,2,4,6,8,10,12 +commap 14 sim.conf >& sim1.log & 
aprun -n 1 -N 1 -d 8 namd2 ++ppn 7 +setcpuaffinity +pemap 0,2,4,6,8,10,12 +commap 14 sim.conf >& sim2.log &

wait
