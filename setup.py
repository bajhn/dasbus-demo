#!/usr/bin/env python3

from setuptools import setup, find_packages

# noinspection HttpUrlsUsage
setup(name='dbdemo',
      version='1.0.0',
      description='Dasbus memory leak demonstrator',
      author='Bruce Johnson',
      url='http://www.example.com',
      packages=find_packages(),
      include_package_data=False,
      requires=['dasbus', 'pygobject'],
      entry_points={'console_scripts': ['dbdemo_server=dbdemo.dbdemo_server:main',
                                        'dbdemo_client=dbdemo.dbdemo_client:main']},
      data_files=[('/lib/systemd/system', ['data/dbdemo.service']),
                  ('/etc/dbus-1/system.d', ['data/dbdemo.conf'])],
      )
