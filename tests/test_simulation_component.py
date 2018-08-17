from htbac import Protocol, Simulation, System, AbFile
from operator import mul
import pytest


def test_simulation_component():

    s0 = Simulation(name='minimizer')
    s0.engine = 'titan_orte'
    s0.processes = 1
    s0.threads_per_process = 16
    s0.add_ensemble('replica', range(5))
    pdb = AbFile('systems/ptp1b-l1-l2-complex.pdb', tag='pdb')
    top = AbFile('systems/ptp1b-l1-l2-complex.top', tag='topology')
    tag = AbFile('systems/ptp1b-l1-l2-tags.pdb', tag='alchemicaltags')
    cor = AbFile('systems/ptp1b-l1-l2-complex.inpcrd', tag='coordinate')
    system = System(name='ptp1b-l1-l2', files=[pdb, top, tag, cor])
    s0.system = system
    
    assert s0.name == 'minimizer'
    assert s0.engine == 'titan_orte'

    assert s0.system.name == 'ptp1b-l1-l2'
    assert s0._processes == 1
    assert s0._threads_per_process == 16
    len_ensemble = reduce(mul, (len(v) for v in s0._ensembles.itervalues()), 1)
    assert s0.cpus == s0.threads_per_process * s0._processes * len_ensemble
    assert s0.shared_data == ['systems/ptp1b-l1-l2-complex.pdb', 'systems/ptp1b-l1-l2-complex.top', 'systems/ptp1b-l1-l2-tags.pdb', 'systems/ptp1b-l1-l2-complex.inpcrd']
    s1 = Simulation(name='equilibrate')

    
test_simulation_component()