## Instructions for running ESMACS/TIES on VM

### Before Execution:

#### Setup the system files 

* Create a folder for each system which includes script, default configs, system
files 

* [RFE system files](https://github.com/radical-cybertools/htbac/tree/master/examples/systems/54353507-54150798)

* [ESMACS system files](https://github.com/radical-cybertools/htbac/tree/master/examples/systems/esmacs-pde2-4d08-l1)

* [RFE default files](https://github.com/radical-cybertools/htbac/tree/master/examples/default_configs/rfe/54353507-54150798)

* [ESMACS default configurations](https://github.com/radical-cybertools/htbac/tree/master/examples/default_configs/esmacs/esmacs-pde2-4d08-l1)

* Update script with the correct paths for system files as shown in [ties.py](https://github.com/radical-cybertools/htbac/blob/master/examples/54353507-54150798.py) and [esmacs.py](https://github.com/radical-cybertools/htbac/blob/master/examples/esmacs-pde2-4d08-l1.py)
* Modify the parameters for each simulation step accordingly 
* Modify the walltime in `ht.run(walltime=2880)` 
* Upload folder VM (sftp)


### Execution Instructions: 

* `ssh <username>@149.165.156.58`
* renew proxy : `myproxy-logon -s tfca.ncsa.illinois.edu -p 7512 -t 1000 -l <user>`
* `tmux new -s <session_name> 
* `source /home/<user>/htbac/venv/bin/active`
* `cd <uploaded_folder>`
* python <script.py>
