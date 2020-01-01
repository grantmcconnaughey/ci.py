import logging
import os
import re

from . import git


logger = logging.getLogger(__name__)


class CIProviderBase(object):
    """Interface for all CI provider classes"""

    name = None
    detection_env_var = None

    @property
    def pr(self):
        raise NotImplementedError

    @property
    def repo(self):
        raise NotImplementedError

    @property
    def commit_sha(self):
        raise NotImplementedError


# https://docs.travis-ci.com/user/environment-variables
class Travis(CIProviderBase):

    name = 'Travis CI'
    detection_env_var = 'TRAVIS'

    @property
    def pr(self):
        pr = os.environ['TRAVIS_PULL_REQUEST']
        if pr == 'false':
            return None
        else:
            return pr

    @property
    def repo(self):
        return os.environ['TRAVIS_REPO_SLUG']

    @property
    def commit_sha(self):
        return os.environ['TRAVIS_PULL_REQUEST_SHA']


# https://circleci.com/docs/1.0/environment-variables
class CircleCI(CIProviderBase):

    name = 'Circle CI'
    detection_env_var = 'CIRCLECI'

    @property
    def pr(self):
        return os.environ['CIRCLE_PR_NUMBER']

    @property
    def repo(self):
        return (os.environ['CIRCLE_PROJECT_USERNAME'] +
                '/' +
                os.environ['CIRCLE_PROJECT_REPONAME'])

    @property
    def commit_sha(self):
        return os.environ['CIRCLE_SHA1']


# https://www.appveyor.com/docs/environment-variables
class AppVeyor(CIProviderBase):

    name = 'AppVeyor'
    detection_env_var = 'APPVEYOR'

    @property
    def pr(self):
        return os.environ['APPVEYOR_PULL_REQUEST_NUMBER']

    @property
    def repo(self):
        return os.environ['APPVEYOR_REPO_NAME']

    @property
    def commit_sha(self):
        return os.environ['APPVEYOR_REPO_COMMIT']


# http://docs.shippable.com/ci/env-vars/#stdEnv
class Shippable(CIProviderBase):

    name = 'Shippable'
    detection_env_var = 'SHIPPABLE'

    @property
    def pr(self):
        return os.environ['PULL_REQUEST']

    @property
    def repo(self):
        return os.environ['SHIPPABLE_REPO_SLUG']

    @property
    def commit_sha(self):
        return os.environ['COMMIT']


# https://semaphoreci.com/docs/available-environment-variables.html
class Semaphore(CIProviderBase):

    name = 'Semaphore'
    detection_env_var = 'SEMAPHORE'

    @property
    def pr(self):
        return os.environ['PULL_REQUEST_NUMBER']

    @property
    def repo(self):
        return os.environ['SEMAPHORE_REPO_SLUG']

    @property
    def commit_sha(self):
        return os.environ['REVISION']


# https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
class CodeBuild(CIProviderBase):

    name = 'CodeBuild'
    detection_env_var = 'CODEBUILD_BUILD_ID'

    REPO_REGEX = r'.+github\.com/(?P<repo>.+\/.+)\.git'

    @property
    def pr(self):
        # CODEBUILD_SOURCE_VERSION=pr/1
        return os.environ['CODEBUILD_SOURCE_VERSION'].split('/')[1]

    @property
    def repo(self):
        # CODEBUILD_SOURCE_REPO_URL=https://github.com/owner/repo.git
        match = re.match(self.REPO_REGEX,
                         os.environ['CODEBUILD_SOURCE_REPO_URL'])
        return match.group('repo')

    @property
    def commit_sha(self):
        return git.head()


# https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables
# Note: variables with '.' in the name will have dot replaced with underscore
# in actual environment
class AzureDevOps(CIProviderBase):

    name = 'Azure DevOps'
    detection_env_var = 'AZURE_HTTP_USER_AGENT'

    @property
    def pr(self):
        return os.environ.get('SYSTEM_PULLREQUEST_PULLREQUESTNUMBER', None)

    @property
    def repo(self):
        return os.environ['BUILD_REPOSITORY_ID']

    @property
    def commit_sha(self):
        return os.environ['BUILD_SOURCEVERSION']


# https://docs.tea-ci.org/usage/variables/
class Drone(CIProviderBase):

    name = 'Drone CI'
    detection_env_var = 'DRONE'

    @property
    def pr(self):
        return os.environ.get('DRONE_PULL_REQUEST', None)

    @property
    def repo(self):
        return os.environ['DRONE_REPO']

    @property
    def commit_sha(self):
        return os.environ['DRONE_COMMIT']


# https://help.github.com/en/actions/automating-your-workflow-with-github-actions/using-environment-variables
class GitHubActions(CIProviderBase):

    name = 'GitHub Actions'
    detection_env_var = 'GITHUB_ACTIONS'

    @property
    def pr(self):
        ref = os.environ.get('GITHUB_REF')
        if ref:
            # On PRs, GITHUB_REF takes the format refs/pull/:prNumber/merge
            return ref.split('/')[2]
        else:
            return None

    @property
    def repo(self):
        return os.environ['GITHUB_REPOSITORY']

    @property
    def commit_sha(self):
        return os.environ['GITHUB_SHA']


def find_ci_provider():
    ci_providers = [
        (Travis.detection_env_var, Travis),
        (CircleCI.detection_env_var, CircleCI),
        (AppVeyor.detection_env_var, AppVeyor),
        (Shippable.detection_env_var, Shippable),
        (Semaphore.detection_env_var, Semaphore),
        (CodeBuild.detection_env_var, CodeBuild),
        (AzureDevOps.detection_env_var, AzureDevOps),
        (Drone.detection_env_var, Drone),
        (GitHubActions.detection_env_var, GitHubActions),
    ]

    for ci_env_var, ci_cls in ci_providers:
        if ci_env_var in os.environ:
            logger.info('CI {} detected'.format(ci_cls.__name__))
            return ci_cls()
    else:
        logger.info('No CI detected')
        return None


def is_ci():
    return find_ci_provider() is not None


def is_pr():
    ci_provider = find_ci_provider()
    if ci_provider:
        return ci_provider.pr is not None
    else:
        return False


def _get_ci_attribute_or_None(attribute):
    ci_provider = find_ci_provider()
    if ci_provider:
        return getattr(ci_provider, attribute)
    else:
        return None


def name():
    return _get_ci_attribute_or_None('name')


def pr():
    return _get_ci_attribute_or_None('pr')


def repo():
    return _get_ci_attribute_or_None('repo')


def commit_sha():
    return _get_ci_attribute_or_None('commit_sha')
