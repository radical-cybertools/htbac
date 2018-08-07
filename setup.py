#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='htbac',
      version='0.2',
      description='High Throughput Binding affinity calculator',
      url='https://github.com/radical-cybertools/radical.htbac',
      license='MIT',
      packages=find_packages(),
      package_data={'': ['*.yaml', 'protocols/default-configs/*/*']},
      install_requires=['numpy', 'parmed', 'PyYAML', 'click'],
      zip_safe=False,
      entry_points={
            'console_scripts': ['progress=htbac.progress:progress'],
            }
      )
