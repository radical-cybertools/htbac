from radical.entk import Stage, Task

from .simulation import Chainable, Simulation


class DataAggregate(Chainable):

    def __init__(self, extension):
        self.extension = extension
        self.input_sim = None
        self.name = "aggregate"

    def generate_task(self):

        assert isinstance(self.input_sim, Simulation)

        task = Task()
        task.name = self.name

        task.executable = ["tar", "czvfh"]
        task.arguments = ["data.tgz", "*"]
        task.cpu_reqs = {'processes': 1,
                         'process_type': None,
                         'threads_per_process': 1,
                         'thread_type': None
                         }

        links = [self.input_sim.output_data([self.extension], **x) for x in self.input_sim._ensemble_product()]
        links = [l for link in links for l in link]
        task.link_input_data.extend(links)

        return task

    def generate_stage(self):
        s = Stage()
        s.name = self.name
        s.add_tasks({self.generate_task()})
        return s

    def add_input_simulation(self, input_sim):
        self.input_sim = input_sim
