import os
from radical.entk import Pipeline, Stage, Task

from .engine import Engine

class Simulation(object):

    def __init__(self):
        self.engine = None
        self.system = None
        self.replica = 0
        self.step = 0
        self.input_data = None
        self.input_name = None
        self.config = None

        # Simulation specific
        self.numsteps = None
        self.cutoff = None
        self.water_model = None

        self._cores = None

    def generate_task(self):

        task = Task()
        task.name = self.name

        task.pre_exec = self.engine.pre_exec
        task.executable = self.engine.executable
        task.arguments = self.engine.arguments
        task.mpi = self.engine.uses_mpi
        task.cores = self.cores

        task.arguments.append(os.path.basename(self.config))
        task.copy_input_data = ['$SHARED/'.format(os.path.basename(self.config))]

        task.post_exec = ['echo {} > simulation.desc'.format(self.name)]

        task.link_input_data = self.system.file_paths(relative_to="$SHARED") + self.input_data
        task.pre_exec += ["sed -i 's/{}/{}/g' {}".format(k, w, os.path.basename(self.config)) for k, w in self.settings.items()]

        return task

    @property
    def cores(self):
        return self.engine.cores or self._cores

    @cores.setter
    def cores(self, value):
        if self.engine and self.engine.cores and self.engine.cores != value:
            raise ValueError("The simulation's engine has a default core count. You cannot change this!")

        self._cores = value

    @property
    def name(self):
        if self.system is None or self.replica is None:
            raise ValueError('The simulation does not have all the necessary information yet')

        return 'system-{}-step-{}-replica-{}'.format(self.system.name, self.step, self.replica)

    def set_engine_for_resource(self, resource):
        self.engine = Engine.from_dictionary(**resource[self.engine])

    def settings(self):
        return dict(BOX_X=self.system.box[0], BOX_Y=self.system.box[1], BOX_Z=self.system.box[2],
                    SYSTEM=self.system.name, STEP=self.numsteps, CUTOFF=self.cutoff,
                    SWITCHING=self.cutoff - 2.0, PAIRLISTDIST=self.cutoff + 1.5,
                    WATERMODEL=self.water_model,
                    INPUT=self.input_name, OUTPUT=self.name)

    def __repr__(self):
        return self.name

    def generate_pipeline(self):
        p = Pipeline()
        p.name = self.name

        s = Stage()
        s.name = str(self.step)

        t = self.generate_task()

        s.add_tasks(t)

        p.add_stages(s)

        return p

    @property
    def shared_data(self):
        return [self.config] + self.system.shared_data
