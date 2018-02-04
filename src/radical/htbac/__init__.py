import os

# Setting the environment variables so you don't have to.

os.environ['RADICAL_ENMD_PROFILING'] = '1'
os.environ['RADICAL_PILOT_PROFILE'] = 'True'
os.environ['RADICAL_ENMD_PROFILE'] = 'True'
os.environ['RADICAL_ENTK_VERBOSE'] = 'DEBUG'
os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://htbac:htbac@ds251287.mlab.com:51287/htbac-inspire-1'

os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'

os.environ['LD_PRELOAD'] = '/lib64/librt.so.1'

# Version
from radical.htbac.version import version, __version__

from radical.htbac.htbac import Runner
from radical.htbac.esmacs import Esmacs
from radical.htbac.ties import Ties
from radical.htbac.ties_eq import TiesEquilibration
from radical.htbac.ties_prod import TiesProduction
from radical.htbac.ties_full_analysis import TiesAnalysis, AdaptiveQuadrature




