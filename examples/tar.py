from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------
#
_KERNEL_INFO = {
    "name":         "tar",                  # Mandatory
    "description":  "Expands the given tar archive",
    "arguments":   {"--directory=":
                        {
                        "mandatory": True,
                        "description": "The folder to tar"
                        },
                    "--tarname=":
                        {
                        "mandatory": True,
                        "description": "The tar name"
                        },
                    },
    "machine_configs":
    {
        "*": {
            "environment"   : None,
            "pre_exec"      : None,
            "executable"    : "tar",
            "uses_mpi"      : False
        }
    }
}

# ------------------------------------------------------------------------------
#
class TarKernel(KernelBase):

    def __init__(self):

        super(TarKernel, self).__init__(_KERNEL_INFO)
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
        arguments  = ['-l', '-c', 'tar -hczf {input1}.tgz -C {input2}/replicas .'.format(input1 = self.get_arg("--tarname="), input2 = self.get_arg("--directory="))]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = None
