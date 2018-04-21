from radical.entk import Pipeline


class Protocol(object):

    def __init__(self):
        self._simulations = list()

    def add_simulation(self, simulation):

        if self._simulations:
            simulation.input_sim = self._simulations[-1]

        self._simulations.append(simulation)

    def generate_pipeline(self):
        p = Pipeline()
        p.name = 'protocol'
        p.add_stages([s.generate_stage() for s in self._simulations])

        return p


