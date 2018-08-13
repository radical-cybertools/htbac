
from htbac import Protocol, Simulation, System

# system = System(prefix='systems/ptp1b-l1-l2')

def test_protocol_component():

    p = Protocol()
    s0 = Simulation(name='minimizer')
    s0.system = None

    s1 = Simulation(name='equilibrate')
    assert p._simulations == list()

test_protocol_component()