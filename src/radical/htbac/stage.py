from radical.entk import Stage

from .simulation import Simulation
from .system import System


class SimulationStage(object):

    def __init__(self):
        self.template_simulation = None
        self.ensembles = dict()

    def generate_stage(self):

        s = Stage()

        for attribute, values in self.ensembles.items():

            tasks = set()

            for value in values:
                setattr(self.template_simulation, attribute, value)
                tasks.add(self.template_simulation.generate_task())

            s.add_tasks(tasks)

        return s


def main():

    system1 = System(prefix='nilotinib-e255k')
    system2 = System(prefix='nilotinib-e255b')

    sim = Simulation()
    sim.engine = 'namd_openmp_cuda'
    sim.config = 'esmacs-0.conf'

    sim.numsteps = 1000
    sim.cutoff = 10.0
    sim.water_model = 'tip4'

    minimize = SimulationStage()
    minimize.template_simulation = sim
    minimize.ensembles = {"replica": range(5),
                          "system": [system1, system2]}
