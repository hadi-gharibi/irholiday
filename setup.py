#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements =[]
requirements = ['requests',
                  'pandas',
                  'beautifulsoup4',
                  'umalqurra',
                  'convertdate',
                  'convert_numbers',
                  'jdatetime']

test_requirements = [ ]

setup(
    author="hadi gharibi",
    author_email='hady.gharibi@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Pandas Datafarme data from time.ir",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='irholiday',
    name='irholiday',
    packages=find_packages(include=['irholiday']),
    setup_requires=setup_requirements,
    url='https://github.com/hadi-gharibi/irholiday',
    version='0.1.8',
    zip_safe=False,
    scripts=['bin/irholiday2csv'],
)
