#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Grant McConnaughey",
    author_email='grantmcconnaughey@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Python toolkit for working with Continuous Integration services.',
    install_requires=requirements,
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='ci',
    name='ci-py',
    packages=find_packages(include=['ci', 'ci.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/grantmcconnaughey/ci.py',
    version='1.0.0',
    zip_safe=False,
)
