
## Instructions for running OpenMM (we recommend a designated VM)

### Before Execution:

#### Setup 

* Create a folder for each system that includes script, default configs, system files (use the following as templates) 

    * [OpenMM System Example](https://github.com/radical-cybertools/htbac/blob/master/examples/openmm/openmm_example.py#L6-L8) 

    ```
    # Example system
    coord = AbFile('systems/nilotinib-e255k-complex.inpcrd', tag='coordinate')
    top = AbFile('systems/nilotinib-e255k-complex.top', tag='topology')
    system = System(name='nilotinib-e255k', files=[top, coord])
    ```
    * Modify the parameters for each simulation step accordingly: 
    
    ```
    sim.engine = 'openmm'
    sim.system = system
    sim.processes = 1
    sim.threads_per_process = 32
    sim.gpu_processses = 1
    sim.numsteps = 1000

    ```

    * Define the `OpenMM` script [benchmark](https://github.com/radical-cybertools/htbac/blob/master/examples/inputs/benchmark.py#L17-L18) 

    ```
    sim.add_input_file('inputs/benchmark.py', is_executable_argument=True)

    ```
    
    * Modify the walltime and resource accordingly:
    * Check the resource yaml [file](https://github.com/radical-cybertools/htbac/blob/master/htbac/resources.yaml#L274)

    ```
    ht = Runner('xsede.bridges_gpu', comm_server=('two.radical-project.org', 33243))
    ht.add_protocol(sim)
    ht.run(walltime=30, queue =  'GPU')

    ```

### Execution Instructions: 


* `ssh VM`
* renew proxy : `myproxy-logon -l <username> -s myproxy.xsede.org`
* `tmux new -s <session_name>` 
* Create and source VE or Conda Env
* `pip/conda install radical.utils saga-python radical.pilot radical.entk`
* `git clone https://github.com/radical-cybertools/htbac.git`
* `cd htbac`
* `pip install .`


### Runtime Environment Variables for Execution 


* `export RADICAL_PILOT_DBURL=<mongodb://>`
* `export SAGA_PTY_SSH_TIMEOUT=2000`
* `export RADICAL_PILOT_PROFILE=True`
* `export PATH=/usr/sbin:$PATH`
* `export RADICAL_VERBOSE="DEBUG"`
* `export RADICAL_ENTK_PROFILE=True`

### Execution: 

`python openmm_example.py`

### After Execution:

* Each job executed from the VM will create a session folder `rp.*`. This folder contains the output data for each unit (`OpenMM` executable). On `xsede.bridges` this output data is found in the project folder `/pylon5/<project>/<user>/radical.pilot.sandbox/rp.*`




