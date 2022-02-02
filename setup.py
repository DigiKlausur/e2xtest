# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='e2xtest',
    version='0.0.1',
    license='MIT',
    url='https://github.com/DigiKlausur/e2xtest',
    description='Create test cases for Jupyter Notebook assignments',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Tim Metzler',
    author_email='tim.metzler@h-brs.de',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    zip_safe=False,
)
