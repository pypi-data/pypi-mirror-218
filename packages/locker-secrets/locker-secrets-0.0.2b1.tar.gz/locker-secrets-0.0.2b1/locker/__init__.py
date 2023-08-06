from __future__ import absolute_import, division, print_function

import os

from .__about__ import (
    __version__
)


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


# Locker Python bindings


# Configuration variables

access_key = None
api_base = "https://secrets-core.locker.io"
api_version = "v1"
proxy = None
max_network_retries = 0

# Set to either 'debug' or 'info', controls console logging
log = None

# API Resources
from locker.ls_resources import *

# Quick usages
from locker.secret_quick_usage import list, get_secret, create, modify
from locker.environment_quick_usage import list_environments, get_environment, create_environment, modify_environment


