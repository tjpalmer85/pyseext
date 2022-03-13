# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyseext',
    version='0.1.0',
    description='Python Selenium ExtJS - package for helping interact with an ExtJS application from Python using Selenium',
    long_description=readme,
    author='Martyn West',
    author_email='657393+westy@users.noreply.github.com',
    url='https://github.com/westy/pyseext',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'exerciser'))
)
