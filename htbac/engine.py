class Engine(object):

    def __init__(self):
        self.executable = None
        self.pre_exec = None
        self.arguments = None
        self.cpus = None
        self.uses_mpi = None

    @classmethod
    def from_dictionary(cls, **kwargs):
        e = Engine()

        e.executable = kwargs.get('executable')
        e.pre_exec = kwargs.get('pre_exec', list())
        e.arguments = kwargs.get('arguments', list())
        e.cpus = kwargs.get('cpus')
        e.uses_mpi = kwargs.get('uses_mpi')

        return e