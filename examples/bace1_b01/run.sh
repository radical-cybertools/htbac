#!/usr/bin/env bash

#PBS -l walltime=02:00:00
#PBS -l nodes=65:ppn=32:xe
cd $PBS_O_WORKDIR
module swap PrgEnv-cray PrgEnv-gnu
export OMP_NUM_THREADS=1
bash workflow.sh 0 0.0 &
bash workflow.sh 0 0.05 &
bash workflow.sh 0 0.1 &
bash workflow.sh 0 0.2 &
bash workflow.sh 0 0.3 &
bash workflow.sh 0 0.4 &
bash workflow.sh 0 0.5 &
bash workflow.sh 0 0.6 &
bash workflow.sh 0 0.7 &
bash workflow.sh 0 0.8 &
bash workflow.sh 0 0.9 &
bash workflow.sh 0 0.95 &
bash workflow.sh 0 1.0 &
bash workflow.sh 1 0.0 &
bash workflow.sh 1 0.05 &
bash workflow.sh 1 0.1 &
bash workflow.sh 1 0.2 &
bash workflow.sh 1 0.3 &
bash workflow.sh 1 0.4 &
bash workflow.sh 1 0.5 &
bash workflow.sh 1 0.6 &
bash workflow.sh 1 0.7 &
bash workflow.sh 1 0.8 &
bash workflow.sh 1 0.9 &
bash workflow.sh 1 0.95 &
bash workflow.sh 1 1.0 &
bash workflow.sh 2 0.0 &
bash workflow.sh 2 0.05 &
bash workflow.sh 2 0.1 &
bash workflow.sh 2 0.2 &
bash workflow.sh 2 0.3 &
bash workflow.sh 2 0.4 &
bash workflow.sh 2 0.5 &
bash workflow.sh 2 0.6 &
bash workflow.sh 2 0.7 &
bash workflow.sh 2 0.8 &
bash workflow.sh 2 0.9 &
bash workflow.sh 2 0.95 &
bash workflow.sh 2 1.0 &
bash workflow.sh 3 0.0 &
bash workflow.sh 3 0.05 &
bash workflow.sh 3 0.1 &
bash workflow.sh 3 0.2 &
bash workflow.sh 3 0.3 &
bash workflow.sh 3 0.4 &
bash workflow.sh 3 0.5 &
bash workflow.sh 3 0.6 &
bash workflow.sh 3 0.7 &
bash workflow.sh 3 0.8 &
bash workflow.sh 3 0.9 &
bash workflow.sh 3 0.95 &
bash workflow.sh 3 1.0 &
bash workflow.sh 4 0.0 &
bash workflow.sh 4 0.05 &
bash workflow.sh 4 0.1 &
bash workflow.sh 4 0.2 &
bash workflow.sh 4 0.3 &
bash workflow.sh 4 0.4 &
bash workflow.sh 4 0.5 &
bash workflow.sh 4 0.6 &
bash workflow.sh 4 0.7 &
bash workflow.sh 4 0.8 &
bash workflow.sh 4 0.9 &
bash workflow.sh 4 0.95 &
bash workflow.sh 4 1.0 &
wait
exit 0
