## HTBAC Workload

Here are instructions for testing a relative free energy protocol. This workload consists of 
1 `EnTK` pipeline, 2 `EnTK` stages, 1 `EnTK` task per stage. By setup, each task receives 32 cores, but 
this can be modified in `rfe.cores = 32`. Currently, this workload is configured to execute on
Blue Waters with the `aprun` launch method using `rabbitmq` docker instance `33052` on the
RADICAL VM-2. This instance has been reserved for the DA scheduler testing. Also, the walltime
and queue can be configured accordingly using `ht.run(walltime=480, queue='high')`. 
Expect this workload to run for approximately 30 minutes. 

### Instructions: 
* Install following stack:
```
pip install https://github.com/radical-cybertools/radical.utils.git
cd radical.util;git checkout devel;pip install .
pip install https://github.com/radical-cybertools/saga-python.git
cd saga-python;git checkout devel;pip install .
git clone git@github.com:radical-cybertools/radical.pilot.git
cd radical.pilot;git checkout project/DA_scheduler_algo; pip install . 
git clone https://github.com/radical-cybertools/radical.entk.git
cd radical.entk;git checkout feature/tagging;pip install .
git clone git@github.com:radical-cybertools/htbac.git
cd htbac;git checkout tagging;pip install .
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
