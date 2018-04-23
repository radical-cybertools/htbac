from radical.entk import Pipeline


class Protocol(object):

    def __init__(self):
        self._simulations = list()

    def add_simulation(self, simulation):

        # TODO: think of something better to do here.
        simulation.major_name = simulation.major_name + "-{}".format(len(self._simulations))

        if self._simulations:
            simulation.input_sim = self._simulations[-1]

        self._simulations.append(simulation)

    def generate_pipeline(self):
        p = Pipeline()
        p.name = 'protocol'
        p.add_stages([s.generate_stage() for s in self._simulations])

        return p

    def set_engine_for_resource(self, resource):
        for sim in self._simulations:
            sim.set_engine_for_resource(resource)

    @property
    def shared_data(self):
        return (data for sim in self._simulations for data in sim.shared_data)

    @property
    def cores(self):
        return self._simulations[0].cores
