#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'yowsup-celery==0.2.1',
    'listenclosely==0.1.2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='listenclosely-whatsapp',
    version='0.1.1',
    description="ListenClosely service backend to work with Whatsapp",
    long_description=readme + '\n\n' + history,
    author="Juan Madurga",
    author_email='jlmadurga@gmail.com',
    url='https://github.com/jlmadurga/listenclosely-whatsapp',
    packages=[
        'listenclosely_whatsapp',
    ],
    package_dir={'listenclosely_whatsapp':
                 'listenclosely_whatsapp'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='listenclosely-whatsapp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
