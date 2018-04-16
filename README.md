
# High Throughput Binding Affinity Calculator 

Framework supporting Alchemical and Endpoint Free Energy Calculation Protocols\
Support with Blue Waters 
## Installation: 
```
virtualenv $HOME/venv
source $HOME/venv/bin/activate
git clone git@github.com:radical-cybertools/radical.utils.git
cd radical.utils
git checkout devel;pip install .;cd ..
git clone git@github.com:radical-cybertools/saga-python.git
cd saga-python
git checkout devel;pip install .;cd ..
git clone git@github.com:radical-cybertools/radical.pilot.git
cd radical.pilot
git checkout feature/fifo;pip install .;cd ..
git clone https://github.com/radical-cybertools/radical.entk.git
cd radical.entk
git checkout devel;pip install .;cd ..

git clone git@github.com:jdakka/radical.htbac.git
cd radical.htbac
git checkout devel;pip install .;cd ..


## Changing to the `FIFO Scheduler` in RP Agent:
vi radical.pilot/src/radical/pilot/configs/resource_ncsa.json
* Change agent_scheduler: 
`"agent_scheduler"             : "CONTINUOUS_FIFO",` 

pip install parmed
pip install numpy

```
### `dependency-links` are currently added to ensure the user has a working `radical-stack`


