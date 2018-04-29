from pkg_resources import resource_filename


class Esmacs:
    step0 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-0.conf")
    step1 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-1.conf")
    step2 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-2.conf")
    step3 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-3.conf")
    step4 = resource_filename(__name__, "default-configs/esmacs/esmacs-stage-4.conf")
    numsteps = [1000, 30000, 1000, 800000, 2000000]


class Afe:
    step0 = resource_filename(__name__, "default-configs/afe/md2.inp")
    step1 = resource_filename(__name__, "default-configs/afe/res2.inp")
    step2 = resource_filename(__name__, "default-configs/afe/restraint.in")


class Rfe:
    step0 = resource_filename(__name__, "default-configs/rfe/ties-0.conf")
    step1 = resource_filename(__name__, "default-configs/rfe/ties-1.conf")
