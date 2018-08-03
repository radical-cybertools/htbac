from radical.entk import Stage, Task

from .simulation import Chainable, Simulation


class DataAggregate(Chainable):

    def __init__(self, extension):
        self.extension = extension
        self.input_sim = None

    def generate_task(self):

        assert isinstance(self.input_sim, Simulation)

        task = Task()
        task.name = "aggregate"

        task.executable = ["tar", "czvfh"]
        task.arguments = ["data.tgz", "*"]
        task.cpu_reqs = {'processes': 1,
                         'process_type': None,
                         'threads_per_process': 1,
                         'thread_type': None
                         }

        task.link_input_data.extend(self.input_sim.output_data([self.extension], **x) for x in self.input_sim._ensemble_product())

        return task

    def generate_stage(self):
        s = Stage()
        s.name = "aggregate"
        s.add_tasks({self.generate_task()})
        return s

    def add_input_simulation(self, input_sim, clone_settings):
        self.input_sim = input_sim
