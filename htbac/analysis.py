from radical.entk import Stage, Task
from StringIO import StringIO
from .simulation import Chainable

NAMD_TI_ANALYSIS = "namd2_ti.pl"

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



class TiesAnalysis(Chainable):
    def __init__(self, extension, output_name="dg.out"):
        self.output_name = output_name # dg.out
        self.extension = extension  # .alch (output for alchOutFile in NAMD)
        self.name = "analysis"
        Chainable.__init__(self)


         # Analysis stage
        # ==============
        # Calculate the dU/dl value at each lambda window
        def generate_task(self):

            task = Task()
            task.name = self.name

            task.executable = [NAMD_TI_ANALYSIS]
            task.arguments = ['-f', '>', self.output]
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

        
        
class AdaptiveQuadrature(Chainable):
    def __init__(self, output_name, tol=2):
        self.namd_ti = output_name
        self.tol = tol
        self._process_data()

    splits = ['Partition 1 electrostatics',
              'Partition 1 vdW',
              'Partition 2 electrostatics']

    def _process_data(self):
        with open(self.namd_ti) as f:
            data = f.read()
            dfs = list()

            for s in self.splits:
                sp = data.split(s)
                dfs += [pd.read_csv(StringIO(sp[0].replace('\t', ' ')), delim_whitespace=True, usecols=[0, 1])]
                data = sp[1]

            self.p1v = dfs[2]

    def requested_windows(self):
        number_to_add = len(self.p1v)

        while True:
            newp1v = self.p1v.copy(deep=True)

            for index in range(len(self.p1v) - 1):
                dif = abs(self.p1v.loc[index]['dE/dl'] - self.p1v.loc[index + 1]['dE/dl'])
                if dif > self.tol:
                    newld = (self.p1v.loc[index]['Lambda'] + self.p1v.loc[index + 1]['Lambda']) / 2
                    print 'Add new ld at:', newld
                    newp1v.loc[len(newp1v)] = [newld, max(self.p1v.loc[index]['dE/dl'], self.p1v.loc[index + 1]['dE/dl'])]
                    number_to_add -= 1

                    if number_to_add == 0:
                        break

            newp1v.sort_values('Lambda', inplace=True)
            newp1v.reset_index(drop=True, inplace=True)
            self.p1v = newp1v

            if number_to_add == 0:
                break

        return self.p1v['Lambda'].as_matrix()



class GradientBoostClassifier(Chainable):

    def __init__(self):
        self.name = "GradientBoostingClassifier"
        self.hyperparameters = 4
        self.data_path  = '/pylon5/mc3bggp/dakka/hyperspace_data/constellation/constellation/data/fashion'
        self.optimization_file = '/home/jdakka/hyperspace/constellation/constellation/gbm/space4/optimize.py'
        self.results_dir = '/pylon5/mc3bggp/dakka/hyperspace_data/results_space_4'

        Chainable.__init__(self)

    def generate_task(self):

        task = Task()
        task.name = self.name
        task.pre_exec = ['env > env.log', 
        'export PATH=/home/dakka/miniconda3/bin:$PATH', 
        'export LD_LIBRARY_PATH=/home/dakka/miniconda3/lib:$LD_LIBRARY_PATH', 
        'source activate ve_hyperspace']
        task.executable = ['python']
        task.arguments = ['optimize.py', '--data_path', self.data_path, 
                            '--results_dir', self.results_dir]
        task.cpu_reqs = {'processes': self.hyperparameters**2,
                         'process_type': None,
                         'threads_per_process': 32, 
                         'thread_type': 'MPI'
                         }

        task.upload_input_data = [self.optimization_file]

        return task

    def generate_stage(self):
        s = Stage()
        s.name = self.name
        s.add_tasks({self.generate_task()})
        return s