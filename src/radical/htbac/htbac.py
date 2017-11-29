__copyright__   = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__      = "Jumana Dakka <jumanadakka@gmail.com>"
__license__     = "MIT"



import esmacs
import ties
import exceptions
import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager



class Runner():

    def __init__(self):

        self.name = htbac
        self.cores = cores
        self.protocols = list()

    def add_protocol(self, protocol):

        self.protocols.append(protocol)

    @property
    def cores(self):
        """
        Number of cores to be used for the current task

        :getter: return the number of cores
        :setter: assign the number of cores
        :arguments: integer
        """

        return self._cores

    @cores.setter
    def cores(self, val):
        if isinstance(val, int):
            self._cores = val
        else:
            raise TypeError(expected_type=int, actual_type=type(val))


    def run():

        pipelines = set()
        for p in self.protocols:
            pipelines.add(p.generate_pipeline())

        res_dict = {
            'resource': 'ncsa.bw_aprun',
            'walltime': 1440,
            'cores': self._cores,
            'project': 'bamm',
            'queue': 'high',
            'access_schema': 'gsissh'}

        # Create Resource Manager object with the above resource description
        rman = ResourceManager(res_dict)
        rman.shared_data = [rootdir + '.tgz']
        # Create Application Manager
        appman = AppManager(port=32775)

        # Assign resource manager to the Application Manager
        appman.resource_manager = rman

        # Assign the workflow as a set of Pipelines to the Application Manager
        appman.assign_workflow(pipelines)

        # Run the Application Manager
        appman.run()


