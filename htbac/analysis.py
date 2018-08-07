from radical.entk import Stage, Task

from .simulation import Chainable


class DataAggregate(Chainable):

    def __init__(self, extension, output_name="data.tgz"):
        self.extension = extension
        self.output_name = output_name
        self.name = "aggregate"

        Chainable.__init__(self)

    def generate_task(self):

        task = Task()
        task.name = self.name

        task.executable = ["tar", "czvfh"]
        task.arguments = [self.output_name, "*{}".format(self.extension)]
        task.cpu_reqs = {'processes': 1,
                         'process_type': None,
                         'threads_per_process': 1,
                         'thread_type': None
                         }

        links = [self.input_data([self.extension], **x) for x in self._input_sim._ensemble_product()]
        links = [l for link in links for l in link]
        task.link_input_data.extend(links)
        task.download_output_data = [self.output_name]

        return task

    def generate_stage(self):
        s = Stage()
        s.name = self.name
        s.add_tasks({self.generate_task()})
        return s
