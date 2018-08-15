
from htbac import Protocol, Simulation, System
import pytest

# system = System(prefix='systems/ptp1b-l1-l2')

def test_simulation_component():

    s0 = Simulation(name='minimizer')
    s0.system = None
    s0.engine = 'titan_orte'
    s0.processes = 1
    s0.threads_per_process = 16
    s0.add_ensemble('replica', range(5))
    # print type(s0._ensembles)
    print s0._variables

    # top = '../examples/systems/ptp1b-l1-l2-complex.top'
    # cor = '../examples/systems/ptp1b-l1-l2-complex.inpcrd'
    # system = System(name='ptp1b-l1-l2', files=[top, cor])

    # s0.system = system

    assert s0.name == 'minimizer'
    assert s0.engine == 'titan_orte'
    # assert s0.system == system
    assert s0._processes == 1
    # assert s0._ensembles == OrderedDict([('replica', [0, 1, 2, 3, 4])])
    assert s0._variables == None
        


    s1 = Simulation(name='equilibrate')
    
test_simulation_component()