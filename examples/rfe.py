"""Relative free energy calculations

Example implementation using Abigail and NAMD.

"""

from htbac import Runner, System, AbFile, DataAggregate
from htbac.protocols import RFE


def run_rfe():
    pdb = AbFile('systems/ptp1b-l1-l2-complex.pdb', tag='pdb')
    top = AbFile('systems/ptp1b-l1-l2-complex.top', tag='topology')
    tag = AbFile('systems/ptp1b-l1-l2-tags.pdb', tag='alchemicaltags')
    cor = AbFile('systems/ptp1b-l1-l2-complex.inpcrd', tag='coordinate')
    system = System(name='ptp1b-l1-l2', files=[pdb, top, tag, cor])

    p = RFE()
    p.append(DataAggregate(extension=".alch"))

    # Protocol `p` is made up of 3 steps:
    # minimize -> simulate -> aggregate data

    for sim, numsteps in zip(p.simulations(), [5000, 50000]):

        sim.system = system
        sim.engine = 'namd'
        sim.processes = 32
        sim.threads_per_process = 1

        sim.cutoff = 12.0
        sim.switchdist = 10.0
        sim.pairlistdist = 13.5
        sim.numsteps = numsteps

        sim.add_ensemble('replica', range(5))
        sim.add_ensemble('lambdawindow', [1.0, 0.5, 0.0])

        import pdb
        pdb.set_trace()

    ht = Runner('bw_aprun', comm_server=('two.radical-project.org', 33158))
    ht.add_protocol(p)
    ht.run(walltime=480, queue='high')


if __name__ == '__main__':
    run_rfe()
