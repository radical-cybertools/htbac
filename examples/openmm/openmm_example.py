from htbac import Runner, Protocol, Simulation, System, AbFile
from htbac.analysis import GradientBoostClassifier

# Step 0: load system files.

coord = AbFile('systems/nilotinib-e255k-complex.inpcrd', tag='coordinate')
top = AbFile('systems/nilotinib-e255k-complex.top', tag='topology')
system = System(name='nilotinib-e255k', files=[top, coord])

# Step 1: create a Simulation

sim = Simulation()

sim.engine = 'openmm'
sim.system = system
sim.processes = 1
sim.threads_per_process = 32

sim.numsteps = 1000

sim.add_input_file('inputs/benchmark.py', is_executable_argument=True)

# Step 2: Hyperparameter optimization using HyperSpace Gradient Boost Classifier 

# analysis = GradientBoostClassifier()
# analysis.hyperparameters = 4
# analysis.data_path  = '/pylon5/mc3bggp/dakka/hyperspace_data/constellation/constellation/data/fashion'
# analysis.optimization_file = '/home/jdakka/hyperspace/constellation/constellation/gbm/space4/optimize.py'
# analysis.results_dir = '/pylon5/mc3bggp/dakka/hyperspace_data/results_space_4'


ht = Runner('xsede.bridges_gpu', comm_server=('two.radical-project.org', 33243))
ht.add_protocol(sim)
ht.run(walltime=30, queue =  'GPU')
