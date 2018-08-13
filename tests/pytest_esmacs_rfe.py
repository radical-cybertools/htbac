from htbac import Protocol, Simulation, Runner, System, AbFile, DataAggregate
from htbac.protocols import RFE, ESMACS

def test_RFE():

    p = RFE()
    assert len(p._simulations) == 2

    for sim in p.simulations():
        
        sim.engine = None
        sim.system = None

        sim.processes = 1
        sim.threads_per_process = 16
        sim.variables = dict()
        sim.add_ensemble('replica', range(5))
        sim.add_ensemble('lambdawindow', [1.0, 0.5, 0.0])

        sim.cutoff = 12.0
        sim.switchdist = 10.0
        sim.pairlistdist = 13.5

        assert sim._processes == 1
        assert sim._threads_per_process == 16 
        assert len(sim._ensembles['replica']) == 5
        assert type(sim._variables) == dict

def test_ESMACS():

    p = ESMACS()
    assert len(p._simulations) == 4

    for sim in p.simulations():
        
        sim.engine = None
        sim.system = None

        sim.processes = 1
        sim.threads_per_process = 16
        sim.variables = dict()
        sim.add_ensemble('replica', range(25))
        

        sim.cutoff = 12.0
        sim.switchdist = 10.0
        sim.pairlistdist = 13.5
    

        assert sim._processes == 1
        assert sim._threads_per_process == 16 
        assert len(sim._ensembles['replica']) == 25
        assert type(sim._variables) == dict

def test_ordering():

    # tests to make sure ensemble members are created in correct order

    p = RFE()

    assert p._simulations[0].name == "simulation-0"
    assert p._simulations[1].name == "simulation-1"


test_ordering()
