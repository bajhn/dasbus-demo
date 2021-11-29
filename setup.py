#!/usr/bin/env python3

from setuptools import setup, find_packages

# noinspection HttpUrlsUsage
setup(name='mmg',
      version='1.0.0',
      description='Dasbus memory leak demonstrator',
      author='Bruce Johnson',
      url='http://www.example.com',
      packages=find_packages(),
      include_package_data=False,
      requires=['pyudev', 'dasbus', 'pygobject'],
      entry_points={'console_scripts': ['demo_server=dbdemo.demo_server:main',
                                        'demo_client=dbdemo.demo_client:main']},
      data_files=[('/lib/systemd/system', ['data/demo.service']),
                  ('/etc/dbus-1/system.d', ['data/demo.conf'])],
      )
