"""Relative free energy calculations

Example implementation using Abigail and NAMD.

"""

import numpy as np

from htbac import Runner, System, Simulation, Protocol, AbFile
from htbac.protocols import Rfe


def run_rfe():
    pdb = AbFile('systems/ptp1b-l1-l2-complex.pdb', tag='pdb')
    top = AbFile('systems/ptp1b-l1-l2-complex.top', tag='topology')
    tag = AbFile('systems/ptp1b-l1-l2-tags.pdb', tag='alchemicaltags')
    cor = AbFile('systems/ptp1b-l1-l2-complex.inpcrd', tag='coordinate')
    system = System(name='ptp1b-l1-l2', files=[pdb, top, tag, cor])

    p = Protocol(clone_settings=False)


    for step, numsteps in zip(Rfe.steps, [5000, 50000]):

        if step == Rfe.step0:

            rfe = Simulation()
            rfe.system = system
            rfe.engine = 'namd_mpi'
            rfe.processes = 1
            rfe.threads_per_process = 32

            rfe.cutoff = 12.0
            rfe.switchdist = 10.0
            rfe.pairlistdist = 13.5
            rfe.numminsteps = 5000
            rfe.numsteps = numsteps

            rfe.add_input_file(step, is_executable_argument=True)
        
            # To change the number of tasks in this stage change 
            # modify the replica parameter here: 

            rfe.add_ensemble('replica', range(5))
            rfe.add_ensemble('lambdawindow', [1.])
            p.append(rfe)

        if step == Rfe.step1:

            rfe = Simulation()
            rfe.system = system
            rfe.engine = 'namd_mpi'
            rfe.processes = 1
            rfe.threads_per_process = 32

            rfe.cutoff = 12.0
            rfe.switchdist = 10.0
            rfe.pairlistdist = 13.5
            rfe.numminsteps = 5000
            rfe.numsteps = numsteps

            rfe.add_input_file(step, is_executable_argument=True)

            # make sure the number of ensemble members is the same as the 
            # previous step for lfs/tagging purposes 

            rfe.add_ensemble('replica', range(5))
            rfe.add_ensemble('lambdawindow', [1.])
            p.append(rfe)


    ht = Runner('bw_aprun', comm_server = ('two.radical-project.org', 33130))
    ht.add_protocol(p)
    ht.run(walltime = 480, queue = 'high')


if __name__ == '__main__':
    run_rfe()
