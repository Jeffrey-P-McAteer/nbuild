
"""
The nbuild module provides functions which
model, build, test, and report the status
of any given project.
"""

import os
import sys
import subprocess
import platform
import tempfile
import shutil

from nbuild.project import Project
from nbuild.deliverable import *
from nbuild.test import Test
from nbuild.task import *
from nbuild.risk import *


# nbuild cares a great deal about it's public API;
# to prevent people from using/reading about internals they
# have no business using we explicitly define __all__,
# the behaviour of which is documented here: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    # Classes
    'Project',
    'Test',
    
]

# The __pdoc__ dictionary contains
# details for pdoc to respect when
# generating documentation.
# See https://pdoc3.github.io/pdoc/doc/pdoc/#overriding-docstrings-with-__pdoc__&gsc.tab=0
__pdoc__ = {
    'constants': False,
    'deliverable': False,
    'project': False,
    'report': False,
    'task': False,
    'test': False,
}



