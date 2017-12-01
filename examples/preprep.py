from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------
#
_KERNEL_INFO = {
    "name":         "preprep",                  # Mandatory
    "description":  "Preprocesses the bac model",
    "arguments":   {"--modeldir=":
                        {
                        "mandatory": True,
                        "description": "The model directory"
                        },
                    "--replica=":
                        {
                        "mandatory": True,
                        "description": "The model replica"
                        },
                    },
    "machine_configs":
    {
        "*": {
            "environment"   : None,
            "pre_exec"      : None,
            "executable"    : "find",
            "uses_mpi"      : False
        }
    }
}

# ------------------------------------------------------------------------------
#
class PreprepKernel(KernelBase):

    def __init__(self):

        super(PreprepKernel, self).__init__(_KERNEL_INFO)
     	"""Le constructor."""

    # --------------------------------------------------------------------------
    #
    @staticmethod
    def get_name():
        return _KERNEL_INFO["name"]

    def _bind_to_resource(self, resource_key):
        """(PRIVATE) Implements parent class method.
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        executable = "/bin/bash"
        arguments  = ['-l', '-c', 'find -L {input1} -type f -print0 | xargs -0 sed -i \'s/REPX/{input2}/g\' ; mkdir -p {input1}/replicas/rep{input2}/equilibration; touch {input1}/replicas/rep{input2}/equilibration/holder; mkdir -p {input1}/replicas/rep{input2}/simulation; touch {input1}/replicas/rep{input2}/simulation/holder'.format(input1 = self.get_arg("--modeldir="), input2 = self.get_arg("--replica="))]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = None
