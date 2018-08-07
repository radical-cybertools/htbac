from pkg_resources import resource_filename


from .. import Protocol, Simulation


class ConcreteProtocol(Protocol):

    @staticmethod
    def _simulation_from_file(f):
        s = Simulation()
        s.add_input_file(resource_filename(__name__, f), is_executable_argument=True)
        return s


class ESMACS(ConcreteProtocol):

    def __init__(self):
        super(ESMACS, self).__init__([self.minimize(), self.thermal_equilibrate(),
                                      self.equilibrate(), self.production()])

    @classmethod
    def minimize(cls):
        return cls._simulation_from_file("default-configs/esmacs/esmacs-stage-0.conf")

    @classmethod
    def thermal_equilibrate(cls):
        return cls._simulation_from_file("default-configs/esmacs/esmacs-stage-1.conf")

    @classmethod
    def equilibrate(cls):
        return cls._simulation_from_file("default-configs/esmacs/esmacs-stage-3.conf")

    @classmethod
    def production(cls):
        return cls._simulation_from_file("default-configs/esmacs/esmacs-stage-4.conf")


# TODO: afe is not a protocol in this sense, as the two steps can be run in parallel. There should also be a min step.
# class AFE(Protocol):
#
#     def __init__(self):
#         super(AFE, self).__init__([self.simulation_complex(), self.simulation_ligand()])
#
#     @staticmethod
#     def simulation_complex():
#         s = Simulation()
#         s.add_input_file(resource_filename(__name__, "default-configs/rfe/md2.inp"), is_executable_argument=True)
#         return s
#
#     @staticmethod
#     def simulation_ligand():
#         s = Simulation()
#         s.add_input_file(resource_filename(__name__, "default-configs/rfe/res2.inp"), is_executable_argument=True)
#         return s


class RFE(ConcreteProtocol):

    def __init__(self):
        super(RFE, self).__init__([self.minimize(), self.simulation()])

    @classmethod
    def minimize(cls):
        return cls._simulation_from_file("default-configs/rfe/ties-0.conf")

    @classmethod
    def simulation(cls):
        return cls._simulation_from_file("default-configs/rfe/ties-1.conf")
