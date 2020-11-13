
"""
The deliverable module holds the Deliverable class
"""

import tempfile
import subprocess
import hashlib
import os

def hash16(data): # To/do move to util.py
    hash_object = hashlib.md5(bytes(data, 'utf-8'))
    return hash_object.hexdigest()

class Deliverable:
    """
    The Deliverable class holds references to delivered assets.
    These may be queried later by tests and tasks such as build systems
    which need to know CWD data and execution tasks which need deliverable
    file names to execute.
    """
    def __init__(self, type_, **kwargs):
        if not type_:
            raise Exception("Error: Deliverable requires type_")
        self.type_ = type_
        self.kwargs = dict(kwargs)

    def get_cwd(self):
        """
        currently only implemented for deliverable of type 'SW_Repository'.
        Returns a working directory for this deliverable, or raises an
        exception if it does not make sense for this deliverable to have a CWD.
        """
        if self.type_ == 'SW_Repository':
            if self.kwargs['directory']:
                return self.kwargs['directory']

            elif self.kwargs['url']:
                if self.kwargs['use_cache']:
                    # Re-use the same temp dir across runs
                    self.kwargs['directory'] = os.path.join(
                        tempfile.gettempdir(),
                        'nbuild_'+hash16(self.kwargs['url'])
                    )
                else:
                    self.kwargs['directory_o'] = tempfile.TemporaryDirectory()
                    self.kwargs['directory'] = self.kwargs['directory_o'].name

                # TO/DO detect git/svn/zip/tar files + treat appropriately
                cache_exists = os.path.exists(self.kwargs['directory']) and len(os.listdir(self.kwargs['directory'])) > 0
                if not cache_exists:
                    subprocess.run([
                        'git', 'clone', '--depth', '1', self.kwargs['url'], self.kwargs['directory']
                    ], check=True)
                else:
                    subprocess.run([
                        'git', 'pull'
                    ], cwd=self.kwargs['directory'], check=True)

                return self.kwargs['directory']

            else:
                raise Exception('Not enough information given to get/download CWD for SW_Repository')


        else:
            raise Exception('Cannot get_cwd for Deliverable of type_={}'.format(self.type_))


# These constants are merely used as words/types in other systems (mostly for deliverables)
# Avoid using falsey values like "", 0, or [] because we often use None
# values as defaults and test if variables have been set with "if not X: raise Exception('must specify X')"
SW_Application = 1

def SW_Repository(url=None, directory=None, use_cache=False):
    """Creates a Deliverable of type SW_Repository"""
    if not url and not directory:
        raise Exception("SW_Repository created without url or directory, one must be specified.")

    return Deliverable(
        type_='SW_Repository',
        url=url,
        directory=directory,
        use_cache=use_cache,
    )
