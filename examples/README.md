## HTBAC Workload

Here are instructions for testing a relative free energy protocol. This workload consists of 
1 `EnTK` pipeline, 4 `EnTK` stages, 65 `EnTK` tasks. As setup, each task receives 32 cores, but 
this can be modified in `rfe.cores = 128`. Currently, this workload is configured to execute on
Blue Waters with the aprun launch method using `rabbitmq` docker instance `33158` on the
RADICAL VM-2. This instance has been reserved for the DA scheduler testing. Also, the walltime
and queue can be configured accordingly using `ht.run(walltime=480, queue='high')`. 

### Instructions: 
* Install following stack:
```
pip install radical.utils==0.47.4
pip install saga-python==0.47.3
git clone git@github.com:radical-cybertools/radical.pilot.git
git checkout project/DA_scheduler_algo
or 
pip install radical.pilot==0.47.8
pip install radical.entk==0.6.1
git clone git@github.com:radical-cybertools/htbac.git
cd htbac; pip install .
git clone 
```

Set the following environmental variables:

```
export RADICAL_PILOT_DBURL='mongodb://user:user@ds223760.mlab.com:23760/scalability' 
export SAGA_PTY_SSH_TIMEOUT=2000
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENMD_PROFILE=True
export RADICAL_ENMD_PROFILING=1
export RP_ENABLE_OLD_DEFINES=True
export PATH=/usr/sbin:$PATH
export RADICAL_VERBOSE="DEBUG"
```

Blue Waters `myproxy` configuration: 

`myproxy-logon -l <username> -s tfca.ncsa.illinois.edu`
* To run the script: `python rfe.py` 
