#!/usr/bin/env python

import ci
from ci.ci import Travis


def test_is_ci_true(monkeypatch):
    monkeypatch.setenv(Travis.detection_env_var, '1')

    assert ci.is_ci() is True


def test_is_pr_true(monkeypatch):
    monkeypatch.setenv(Travis.detection_env_var, '1')
    monkeypatch.setenv('TRAVIS_PULL_REQUEST', '38')

    assert ci.is_pr() is True


def test_pr(monkeypatch):
    monkeypatch.setenv(Travis.detection_env_var, '1')
    monkeypatch.setenv('TRAVIS_PULL_REQUEST', '39')

    assert ci.pr() == '39'


def test_commit_sha(monkeypatch):
    monkeypatch.setenv(Travis.detection_env_var, '1')
    monkeypatch.setenv('TRAVIS_PULL_REQUEST_SHA', '12345')

    assert ci.commit_sha() == '12345'


def test_name(monkeypatch):
    monkeypatch.setenv(Travis.detection_env_var, '1')

    assert ci.name() == 'Travis CI'
