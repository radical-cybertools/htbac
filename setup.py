#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='htbac',
      version='0.0.1',
      description='High Throughput Binding affinity calculator',
      url='https://github.com/radical-cybertools/radical.htbac',
      license='MIT',
      packages=find_packages(),
      package_data={'': ['*.yaml', 'protocols/default-configs/*.conf']},
      install_requires=['numpy', 'parmed', 'PyYAML'],
      zip_safe=False,
      )
