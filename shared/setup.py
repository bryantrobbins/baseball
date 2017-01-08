from setuptools import setup

setup(name='btr3baseball',
      version='0.1',
      description='Set of python utilities for the Baseball Workbench',
      url='http://github.com/bryantrobbins/baseball',
      author='Bryan Robbins and Contributors',
      author_email='bryantrobbins@gmail.com',
      license='ApacheV2',
      packages=['btr3baseball'],
      install_requires=[
          'rpy2',
          'boto3'
      ],
      zip_safe=False)
