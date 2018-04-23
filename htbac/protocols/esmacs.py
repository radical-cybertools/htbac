from pkg_resources import resource_filename

from ..protocol import Protocol
from ..simulation import EnsembleSimulation

# Constants
_reduced_steps = [100, 5000, 1000, 10, 5000]
_full_steps = [1000, 30000, 1000, 800000, 2000000]


class Esmacs(Protocol):
    def __init__(self):
        super(Esmacs, self).__init__()

        s0 = EnsembleSimulation()
        s0.config = resource_filename(__name__, 'default-configs/esmacs-0.conf')
        s0.add_ensemble('replica', range(25))
        s0.engine = 'namd_openmp_cuda'

        s1 = EnsembleSimulation()
        s1.config = resource_filename(__name__, 'default-configs/esmacs-1.conf')

        self.add_simulation(s1)
