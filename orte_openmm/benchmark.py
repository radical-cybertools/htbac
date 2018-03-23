#!/bin/env python

"""
Benchmark.
"""

from simtk.openmm import app
from simtk import unit, openmm

from parmed.amber import AmberParm

import time


def main():

    prmtop_filename = '/lustre/atlas/scratch/farkaspall/chm126/inspire-data/nilotinib/e255k/build/e255k-complex.top'
    crd_filename = '/lustre/atlas/scratch/farkaspall/chm126/inspire-data/nilotinib/e255k/build/e255k-complex.inpcrd'

    prmtop = AmberParm(prmtop_filename, crd_filename)

    system = prmtop.createSystem(nonbondedMethod=app.PME, nonbondedCutoff=10*unit.angstrom,
                                 constraints=app.HBonds, switchDistance=8*unit.angstrom)

    temperature = 300 * unit.kelvin
    pressure = 1 * unit.atmosphere
    collision_rate = 5 / unit.picosecond
    timestep = 2 * unit.femtosecond

    integrator = openmm.LangevinIntegrator(temperature, collision_rate, timestep)
    barostat = openmm.MonteCarloBarostat(temperature, pressure)
    system.addForce(barostat)

    system.setDefaultPeriodicBoxVectors(*prmtop.box_vectors)

    simulation = app.Simulation(prmtop.topology, system, integrator)

    simulation.context.setPositions(prmtop.positions)
    simulation.context.setVelocitiesToTemperature(temperature)

    print('System contains {} atoms.'.format(system.getNumParticles()))
    print('Using platform "{}".'.format(simulation.context.getPlatform().getName()))

    print('Minimizing energy to avoid clashes.')
    simulation.minimizeEnergy(maxIterations=100)

    print('Initial potential energy is {}'.format(simulation.context.getState(getEnergy=True).getPotentialEnergy()))

    # Warm up the integrator to compile kernels, etc
    print('Warming up integrator to trigger kernel compilation...')
    simulation.step(10)

    # Time integration
    print('Benchmarking...')
    nsteps = 5000
    initial_time = time.time()
    integrator.step(nsteps)
    final_time = time.time()
    elapsed_time = (final_time - initial_time) * unit.seconds
    simulated_time = nsteps * timestep
    performance = (simulated_time / elapsed_time)
    print('Completed {} steps in {}.'.format(nsteps, elapsed_time))
    print('Performance is {} ns/day'.format(performance / (unit.nanoseconds/unit.day)))
    print('Final potential energy is {}'.format(simulation.context.getState(getEnergy=True).getPotentialEnergy()))


if __name__ == '__main__':
    main()