## Instructions for running ESMACS/TIES on VM

### Before Execution:

#### Setup the system files 

* Create a folder for each system which includes script, default configs, system
files 

    * [RFE system files](https://github.com/radical-cybertools/htbac/tree/master/examples/systems/54353507-54150798)

    * [ESMACS system files](https://github.com/radical-cybertools/htbac/tree/master/examples/systems/esmacs-pde2-4d08-l1)

    * [RFE default configurations](https://github.com/radical-cybertools/htbac/tree/master/examples/default_configs/rfe/54353507-54150798)

    * [ESMACS default configurations](https://github.com/radical-cybertools/htbac/tree/master/examples/default_configs/esmacs/esmacs-pde2-4d08-l1)

    * Update script with the correct paths for system files as shown in [ties.py](https://github.com/radical-cybertools/htbac/blob/master/examples/54353507-54150798.py) and [esmacs.py](https://github.com/radical-cybertools/htbac/blob/master/examples/esmacs-pde2-4d08-l1.py)
    ```
    # Example system
    pdb = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.pdb', tag='pdb')
    top = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.top', tag='topology')
    cons = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-f4.pdb', tag='constraint')
    cor = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.crd', tag='coordinate')
    system = System(name='esmacs-pde2-4d08-l1', files=[pdb, top, cons, cor])
    ```
    * Modify the parameters for each simulation step accordingly: 
     ```
      s0 = Simulation(name='stage-0')
      s0.engine = 'namd'
      s0.processes = 32
      s0.threads_per_process = 1
      s0.add_ensemble('replica', range(25))
      s0.add_input_file("default_configs/esmacs/esmacs-pde2-4d08-l1/esmacs-stage-0.conf", is_executable_argument=True)
      s0.system = system`
     ```
    * Modify the walltime accordingly:
      ```
      ht.run(walltime=2880)
      ```
* Upload folder to VM (sftp)

### Execution Instructions: 

* `ssh <username>@149.165.156.58`
* renew proxy : `myproxy-logon -s tfca.ncsa.illinois.edu -p 7512 -t 1000 -l <user>`
* `tmux new -s <session_name> 
* `source /home/<user>/htbac/venv/bin/active`
* `cd <uploaded_folder>`
* python <script.py>
