import numpy as np
import os, sys

from htbac import Runner, System, Simulation, Protocol, AbFile

CUR_STAGE = 1
MAX_STAGES = int(sys.argv[1])


# Import HTBAC modules

from htbac import Protocol, Simulation, System

def run_adaptive():

    pdb = AbFile('systems/ptp1b-l1-l2-complex.pdb', tag='pdb')
    top = AbFile('systems/ptp1b-l1-l2-complex.top', tag='topology')
    tag = AbFile('systems/ptp1b-l1-l2-tags.pdb', tag='alchemicaltags')
    cor = AbFile('systems/ptp1b-l1-l2-complex.inpcrd', tag='coordinate')
    system = System(name='ptp1b-l1-l2', files=[pdb, top, tag, cor])
    
    # Protocol takes arguments

    p = Protocol(clone_settings=False)

    sim1 = Simulation(name='minimization')
    p.append(sim1)
    sim1.engine = 'dummy'

    sim1.system = system
    ht = Runner('local', comm_server=('two.radical-project.org', 33158))
    ht.add_protocol(p)
    ht.run(walltime=480, queue='high')


if __name__ == '__main__':
    run_adaptive()