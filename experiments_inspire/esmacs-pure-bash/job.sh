#!/bin/bash 
#PBS -A chm126
#PBS -N test
#PBS -q debug
#PBS -j oe
#PBS -l walltime=0:20:00
#PBS -l nodes=2


# Pre-executables
module load namd/2.12

export MPICH_PTL_SEND_CREDITS=-1
export MPICH_MAX_SHORT_MSG_SIZE=8000
export MPICH_PTL_UNEX_EVENTS=80000
export MPICH_UNEX_BUFFER_SIZE=100M

cd $MEMBERWORK/chm126/htbac/experiments_inspire/esmacs-pure-bash

# Executable

aprun -n 1 -N 1 -d 8 namd2 ++ppn 7 +setcpuaffinity +pemap 0,2,4,6,8,10,12 +commap 14 sim.conf >& sim1.log &
aprun -n 1 -N 1 -d 8 namd2 ++ppn 7 +setcpuaffinity +pemap 0,2,4,6,8,10,12 +commap 14 sim.conf >& sim2.log &

wait

# Profiling

echo "Command:" > sim.prof
echo "aprun -n 1 -N 1 -d 8 namd2 ++ppn 7 +setcpuaffinity +pemap 0,2,4,6,8,10,12 +commap 14" >> sim.prof

echo "Ns per days:" >> sim.prof
grep "days/ns" sim1.log  | tail -1 | awk {'print 1/$8'} >> sim.prof
grep "days/ns" sim2.log  | tail -1 | awk {'print 1/$8'} >> sim.prof


echo "Wall clock times:" >> sim.prof
grep "WallClock" sim1.log  | awk {'print $2'} >> sim.prof
grep "WallClock" sim2.log  | awk {'print $2'} >> sim.prof


