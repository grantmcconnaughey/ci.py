# ci.py

[![Build Status](https://travis-ci.org/grantmcconnaughey/ci.py.svg?branch=master)](https://travis-ci.org/grantmcconnaughey/ci.py)

A Python library for working with Continuous Integration services. For Python 2.7 and 3.5+.

## Usage

First, `pip` install ci.py:

    $ pip install ci-py

## Available Methods

```python
import ci

ci.is_ci()  # True/False
ci.is_pr()  # True/False
ci.name()  # "Travis CI"
ci.pr()  # "38"
ci.repo()  # "grantmcconnaughey/ci.py"
ci.commit_sha()  # "246249bab34e78a020efc67b626efd6052e754d9"
```

## CI Services

ci.py works with the following CI services:

- Travis CI
- Circle CI
- GitHub Actions
- Drone CI
- AppVeyor
- Shippable
- Semaphore
- AWS CodeBuild
- Azure DevOps

## Running Tests

To run tests, install `tox` and run it from the command line:

```
> tox
```

This will run tests against all of the Python versions defined in `tox.ini`. Note that all of these versions of Python will need to be installed. You can use `pyenv` to install these different versions.
