#!/usr/bin/env python

from setuptools import setup, find_packages

short_version = 0.0

setup_args = {
    'name'             : 'radical.htbac',
    'version'          :  short_version,
    'description'      : "Radical htbac Toolkit.",
    'author'           : 'RADICAL Group at Rutgers University',
    'author_email'     : 'jumanadakka@gmail.com',
    'maintainer'       : "Jumana Dakka",
    'maintainer_email' : 'jumanadakka@gmail.com',
    'url'              : 'https://github.com/radical-cybertools/radical.htbac',
    'license'          : 'MIT',
    'keywords'         : "binding affinity calculator workflow execution",
    'packages'         : find_packages(),
    'package_data'     : {'': ['*.yaml', 'default-configs/*.conf']},
    'install_requires' : ['parmed', 'PyYAML'],
    'zip_safe'         : False,
}

setup(**setup_args)
