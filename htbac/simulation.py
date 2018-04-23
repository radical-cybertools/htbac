import os
import re
from operator import mul
from collections import OrderedDict
from itertools import product, izip

from radical.entk import Pipeline, Stage, Task

from .engine import Engine


class BaseSimulation(object):

    def __init__(self):
        self.major_name = 'stage'
        self.minor_name = 'simulation'
        self.engine = None
        self.system = None
        self._input_sim = None
        self._input_files = set()
        self._arguments = list()
        self._cores = 0
        self._placeholders = set()

    _path = "$Pipeline_{pipeline}_Stage_{stage}_Task_{task}"
    _sed = "sed -i 's/<{}>/{}/g' {}"
    _r = re.compile("<(\S+)>")

    def generate_task(self):

        task = Task()
        task.name = self.minor_name

        task.pre_exec += self.engine.pre_exec
        task.executable += self.engine.executable
        task.arguments += self.engine.arguments
        task.mpi = self.engine.uses_mpi
        task.cores = self._cores

        task.arguments.extend(self._arguments)
        task.copy_input_data.extend(os.path.join('$SHARED', arg) for arg in self._arguments)

        task.post_exec = ['echo "{}" > simulation.desc'.format(self)]

        task.link_input_data = self.system.file_paths(relative_to="$SHARED") + self.input_data

        task.pre_exec.extend(self._sed.format(k, w, f) for k, w in self._settings.iteritems() for f in self._arguments)

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
        return list(self._input_files) + self.system.shared_data

    @property
    def input_data(self):
        if self._input_sim is None:
            return list()
        # TODO: pipeline name has to be fixed!
        path = self._path.format(stage=self._input_sim.major_name, task=self.minor_name, pipeline='protocol')
        return [os.path.join(path, self._input_sim.major_name+s) for s in ['.coor', '.xsc', '.vel']]

    @property
    def _settings(self):

        settings = {k: getattr(self, k) for k in self._placeholders}

        input_name = self._input_sim.major_name if self._input_sim else str()
        settings.update(dict(box_x=self.system.box[0], box_y=self.system.box[1], box_z=self.system.box[2],
                        system=self.system.name, input=input_name, output=self.major_name))

        return settings

    def set_input_simulation(self, input_sim, copy_setup=True):
        self._input_sim = input_sim

        if copy_setup:
            self.engine = input_sim.engine
            self.cores = input_sim.cores

            for attr in input_sim._placeholders:
                self.add_placeholder(attr, getattr(input_sim, attr))

    def add_placeholder(self, name, value=None):
        if not hasattr(self, name):
            setattr(self, name, value)

        self._placeholders.add(name)

    def add_input_file(self, input_file, is_executable_argument, auto_detect_variables=True):
        self._input_files.add(input_file)

        if is_executable_argument:
            self._arguments.append(os.path.basename(input_file))

        if auto_detect_variables:
            with open(input_file) as f:
                for var in set(re.findall(self._r, f.read())):
                    self.add_placeholder(var)

    def __len__(self):
        return 1


class EnsembleSimulation(BaseSimulation):

    def __init__(self):
        super(EnsembleSimulation, self).__init__()

        self._ensembles = OrderedDict()

    def add_ensemble(self, key, values):
        """
        Add a parameter to the simulation that you want multiple values to be run with. For example
        running multiple systems with the same configuration, or trying out a range of cutoff
        distances to see which one works best. This is very powerful!
        :param key:
        :param values:
        :return:
        """
        if not hasattr(self, key):
            self.add_placeholder(key)

        self._ensembles[key] = values

    def set_input_simulation(self, input_sim, copy_setup=True):
        if not isinstance(input_sim, EnsembleSimulation):
            raise ValueError('Input simulation has to have ensembles too!')

        if self._ensembles:
            raise ValueError('Simulation ensemble will be inherited. Do not set it!')

        for key, value in input_sim._ensembles.iteritems():
            self.add_ensemble(key, value)

        super(EnsembleSimulation, self).set_input_simulation(input_sim, copy_setup=copy_setup)

    def generate_task(self, **ensembles):

        for attribute, value in ensembles.iteritems():
            if getattr(self, attribute):
                raise AttributeError('Attribute {} should not have been set!'.format(attribute))

            setattr(self, attribute, value)

        generic = self.minor_name

        ens_name = reduce(lambda x, y: '{}-{}'.format(x, y), ('{}-{}'.format(k, w) for k, w in ensembles.iteritems()))

        self.minor_name = self.minor_name + ens_name

        t = super(EnsembleSimulation, self).generate_task()

        # Reset everything to how it was before
        self.minor_name = generic
        for attribute in ensembles.keys():
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
            return list(self._input_files) + [d for s in self._ensembles['system'] for d in s.shared_data]
        else:
            return super(EnsembleSimulation, self).shared_data
