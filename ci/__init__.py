__author__ = 'Grant McConnaughey'
__email__ = 'grantmcconnaughey@gmail.com'
__version__ = '1.0.0'

from .ci import (  # noqa: F401
    is_ci,
    is_pr,
    name,
    pr,
    repo,
    commit_sha
)
