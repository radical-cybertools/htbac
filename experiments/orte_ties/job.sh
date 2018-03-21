#!/bin/bash

export RADICAL_PILOT_DBURL='mongodb://htbac:htbac@ds251287.mlab.com:51287/htbac-inspire-1'
export SAGA_PTY_SSH_TIMEOUT=2000
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENMD_PROFILE=True
export RADICAL_ENMD_PROFILING=1
export RP_ENABLE_OLD_DEFINES=True

export RADICAL_ENTK_VERBOSE='DEBUG'
export RADICAL_SAGA_VERBOSE='DEBUG'
export RADICAL_PILOT_VERBOSE='DEBUG'

export LD_PRELOAD='/lib64/librt.so.1'

module swap PrgEnv-gnu/5.2.82
module load tcl_tk/8.5.8
module unload cray-mpich
module load cmake
module load rca 
                                
module load python/2.7.9
module load python_pip/8.1.2
module load python_virtualenv/12.0.7

#python /lustre/atlas/scratch/farkaspall/chm126/htbac/experiments_inspire/esmacs-nilotinib.py
python ties_8_instances.py


