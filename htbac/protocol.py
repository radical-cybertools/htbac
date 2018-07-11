import logging
from collections import MutableSequence

from radical.entk import Pipeline

from .simulation import Chainable, Simulatable


class Protocol(Simulatable, MutableSequence):
    """Protocol is a list of simulatable elements that can be chained.

    """

    def __init__(self, clone_settings):
        self._simulations = list()
        self.clone_settings = clone_settings

    def __getitem__(self, item):
        return self._simulations[item]

    def __setitem__(self, key, value):
        raise IndexError('Protocol elements cannot be changed.')

    def __delitem__(self, key):
        raise IndexError('Protocol elements cannot be deleted')

    def insert(self, index, simulation):
        if index != len(self):
            raise IndexError('New simulation can only be appended to end of protocol!')

        if len(self):
            logging.info('Simulation appended to protocol.')
            simulation.add_input_simulation(self[-1], clone_settings=self.clone_settings)

        simulation.name += "-{}".format(len(self))

        self._simulations.insert(index, simulation)

    def __len__(self):
        return len(self._simulations)

    def generate_pipeline(self):
        p = Pipeline()
        p.name = 'protocol'
        p.add_stages([s.generate_stage() for s in self])

        return p

    def configure_engine_for_resource(self, resource):
        for sim in self:
            sim.configure_engine_for_resource(resource)

    @property
    def shared_data(self):
        return (data for sim in self for data in sim.shared_data)

    @property
    def cpus(self):
        """

        Returns
        -------
        int
            Number of cpus the first simulation in the protocol requires.
        """
        return self[0].cpus
