from htbac import Runner, Protocol, Simulation, System, AbFile, DataAggregate
from htbac.protocols import RFE, ESMACS # Allows users to utilize pre-defined protocols 

# define system
pdb = AbFile('systems/ptp1b-l1-l2-complex.pdb', tag='pdb')
top = AbFile('systems/ptp1b-l1-l2-complex.top', tag='topology')
tag = AbFile('systems/ptp1b-l1-l2-tags.pdb', tag='alchemicaltags')
cor = AbFile('systems/ptp1b-l1-l2-complex.inpcrd', tag='coordinate')
system = System(name='ptp1b-l1-l2', files=[pdb, top, tag, cor])


# Create simulation steps for relative free energy protocol

# define protocol:
p = Protocol()

# define step 0: 
s0 = Simulation(name='minimizer')
s0.engine = 'namd'
s0.processes = 1
s0.threads_per_process = 16
s0.add_ensemble('replica', range(5))
s0.add_ensemble('lambdawindow', [1.0, 0.5, 0.0]) 
s0.add_input_file("default_configs/rfe/ties-0.conf", is_executable_argument=True)
s0.system = system


s0.cutoff = 12.0
s0.switchdist = 10.0
s0.pairlistdist = 13.5
s0.numsteps = 5000
s0.watermodel = "tip3"

# set all values that have <placeholder> in the *.conf file 
# import pdb
# pdb.set_trace()
# print [k for k, vs in s0._variables.items() for v in vs if s0.get_variable(v) is None]



# append step 0 to protocol:
p.append(s0)

# define step 1: 
s1 = Simulation(name='equilibrate')
s1.engine = 'namd'
s1.processes = 1
s1.threads_per_process = 16
s1.add_ensemble('replica', range(5))
s1.add_ensemble('lambdawindow', [1.0, 0.5, 0.0])
s1.add_input_file("default_configs/rfe/ties-1.conf", is_executable_argument=True)
s1.system = system
s1.watermodel = "tip3"

# <placeholders>
s1.cutoff = 12.0
s1.switchdist = 10.0
s1.pairlistdist = 13.5
s1.numsteps = 50000 


# append step 1 to protocol:
p.append(s1)

ht = Runner('bw_aprun', comm_server=('two.radical-project.org', 33048))

ht.add_protocol(p)
ht.run(walltime=480)
