
# High Throughput Binding Affinity Calculator 

Framework supporting UCL ESMACS/TIES protocols \


## Installation: 
```
virtualenv $HOME/venv
source $HOME/venv/bin/activate
cd htbac
git checkout adaptive
pip install --process-dependency-links --upgrade . 
pip install parmed
pip install numpy
cd experiments/ta_3_1
myproxy-logon -l <user> -s tfca.ncsa.illinois.edu
python ties_super_adapt.py >> debug.log 2>> debug.log
```
### `dependency-links` are currently added to ensure the user has a working `radical-stack`


