class Engine(object):

    def __init__(self):
        self.executable = None
        self.pre_exec = None
        self.arguments = None
        self.processes = None
        self.gpu_processes = None
        self.threads_per_process = None
        self.gpu_threads_per_process = None
        self.uses_mpi = None
        self.gpu_uses_mpi = None

    @classmethod
    def from_dictionary(cls, **kwargs):
        e = Engine()

        e.executable = kwargs.get('executable')
        e.pre_exec = kwargs.get('pre_exec', list())
        e.arguments = kwargs.get('arguments', list())
        e.processes = kwargs.get('processes')
        e.gpu_processes = kwargs.get('gpu_processes')
        e.threads_per_process = kwargs.get('threads_per_process')
        e.gpu_threads_per_process = kwargs.get('gpu_threads_per_process')
        e.uses_mpi = kwargs.get('uses_mpi')
        e.gpu_uses_mpi = kwargs.get('gpu_uses_mpi')


        return e
