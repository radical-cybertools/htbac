import os
from operator import mul
from itertools import product, izip

from radical.entk import Pipeline, Stage, Task

from .engine import Engine


class BaseSimulation(object):

    def __init__(self):
        self.major_name = 'stage'
        self.minor_name = 'simulation'
        self.engine = None
        self.system = None
        self.input_sim = None
        # TODO: automatically detect placeholders in configuration file.
        self.config = None
        self._cores = 0
        self._placeholders = list()

    def generate_task(self):

        task = Task()
        task.name = self.minor_name

        task.pre_exec += self.engine.pre_exec
        task.executable += self.engine.executable
        task.arguments += self.engine.arguments
        task.mpi = self.engine.uses_mpi
        task.cores = self._cores

        task.arguments.append(os.path.basename(self.config))
        task.copy_input_data = [os.path.join('$SHARED', os.path.basename(self.config))]

        task.post_exec = ['echo "{}" > simulation.desc'.format(self)]

        task.link_input_data = self.system.file_paths(relative_to="$SHARED") + self.input_data

        task.pre_exec += ["sed -i 's/<{}>/{}/g' {}".format(k, w, os.path.basename(self.config)) for k, w in
                          self._settings.iteritems()]

        return task

    @property
    def cores(self):
        return self._cores * len(self)

    @cores.setter
    def cores(self, value):
        if isinstance(self.engine, Engine) and self.engine.cores and self.engine.cores != value:
            raise ValueError('Engine has default core count. Do not set simulation cores!')
        self._cores = value

    def set_engine_for_resource(self, resource):
        if not isinstance(self.engine, str):
            raise ValueError('Engine type not set!')

        self.engine = Engine.from_dictionary(**resource[self.engine])

        if self.engine.cores:
            if self.cores and self.cores != self.engine.cores:
                raise ValueError('Engine has default core count. Do not set simulation cores!')

            self.cores = self.engine.cores

    def __repr__(self):
        return self.major_name + self.minor_name

    def generate_stage(self):
        s = Stage()
        s.name = self.major_name
        s.add_tasks(self.generate_task())

        return s

    def generate_pipeline(self):
        p = Pipeline()
        p.name = 'protocol'
        p.add_stages(self.generate_stage())

        return p

    @property
    def shared_data(self):
        return [self.config] + self.system.shared_data

    @property
    def input_data(self):
        if self.input_sim is None:
            return list()

        path = "$Pipeline_{pipeline}_Stage_{stage}_Task_{task}"
        # TODO: pipeline name has to be fixed!
        path.format(stage=self.input_sim.major_name, task=self.minor_name, pipeline='protocol')
        return [os.path.join(path, self.input_sim.name+s) for s in ['.coor', '.xsc', '.vel']]

    @property
    def _settings(self):

        input_name = self.input_sim.major_name if self.input_sim else str()
        settings = dict(box_x=self.system.box[0], box_y=self.system.box[1], box_z=self.system.box[2],
                        system=self.system.name, input=input_name, output=self.major_name)

        settings.update({k: getattr(self, k) for k in self._placeholders})

        return settings

    def add_placeholder(self, name, value=None):
        setattr(self, name, value)
        self._placeholders.append(name)

    def __len__(self):
        return 1


class EnsembleSimulation(BaseSimulation):

    def __init__(self):
        super(EnsembleSimulation, self).__init__()

        self._ensembles = {}
        self._input_sim = None

    def add_ensemble(self, key, values):
        """
        Add a parmeter to the simulation that you want multiple values to be run with. For example
        running multiple systems with the same configuration, or trying out a range of cutoff
        distances to see which one works best. This is very powerful!
        :param key:
        :param values:
        :return:
        """
        if not hasattr(self, key):
            self.add_placeholder(key)

        self._ensembles[key] = values
        self.minor_name += "-{key}-{{{key}}}".format(key=key)

    @property
    def input_sim(self):
        return self._input_sim

    @input_sim.setter
    def input_sim(self, sim):
        if sim is not None:
            if not isinstance(sim, EnsembleSimulation):
                raise ValueError('Input simulation has to have ensembles too!')

            if self._ensembles:
                raise ValueError('Simulation ensemble will be inherited. Do not set it!')

            for key, value in sim._ensembles.iteritems():
                self.add_ensemble(key, value)

        self._input_sim = sim

    def generate_task(self, **kwargs):

        for attribute, value in kwargs.iteritems():
            if getattr(self, attribute):
                raise AttributeError('Attribute {} should not have been set!'.format(attribute))

            setattr(self, attribute, value)
        generic = self.minor_name

        self.minor_name = self.minor_name.format(**kwargs)

        t = super(EnsembleSimulation, self).generate_task()

        self.minor_name = generic
        for attribute in kwargs.keys():
            setattr(self, attribute, None)

        return t

    def generate_stage(self):
        s = Stage()
        s.name = self.major_name
        s.add_tasks({self.generate_task(**x) for x in self._ensemble_product()})

        return s

    def _ensemble_product(self):
        return (dict(izip(self._ensembles, x)) for x in product(*self._ensembles.itervalues()))

    def __len__(self):
        return reduce(mul, (len(v) for v in self._ensembles.itervalues()), 1)

    @property
    def shared_data(self):
        if 'system' in self._ensembles:
            return [self.config] + [d for s in self._ensembles['system'] for d in s.shared_data]
        else:
            return super(EnsembleSimulation, self).shared_data
