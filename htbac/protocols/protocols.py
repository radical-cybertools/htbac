from pkg_resources import resource_filename


class Esmacs:

    def __init__(self):
        self.step0 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-0.conf")
        self.step1 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-1.conf")
        self.step2 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-2.conf")
        self.step3 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-3.conf")
        self.step4 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-4.conf")
        self.numsteps = [1000, 30000, 1000, 800000, 2000000]


class Afe:

    def __init__(self):
        self.step0 = resource_filename(__name__, "default-configs/afe/md2.inp")
        self.step1 = resource_filename(__name__, "default-configs/afe/res2.inp")
        self.step2 = resource_filename(__name__, "default-configs/afe/restraint.in")
