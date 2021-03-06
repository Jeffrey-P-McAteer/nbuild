
"""
The deliverable module holds the Deliverable class
"""

import tempfile
import subprocess
import os
import html

import zipfile
# import tarfile
# import bz2
# import lzma
import io

# python3 -m pip install --user requests
import requests

from nbuild.util import hash16, deflate_dir

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

    def get_cwd(self): # pylint: disable=too-many-branches
        """
        currently only implemented for deliverable of type 'SW_Repository'.
        Returns a working directory for this deliverable, or raises an
        exception if it does not make sense for this deliverable to have a CWD.
        """
        if self.type_ == 'SW_Repository':
            if self.kwargs['directory']:
                return self.kwargs['directory']

            elif self.kwargs['url']:
                url = self.kwargs['url']
                if self.kwargs['use_cache']:
                    # Re-use the same temp dir across runs
                    self.kwargs['directory'] = os.path.join(
                        tempfile.gettempdir(),
                        'nbuild_'+hash16(url)
                    )
                else:
                    self.kwargs['directory_o'] = tempfile.TemporaryDirectory()
                    self.kwargs['directory'] = self.kwargs['directory_o'].name

                cache_exists = os.path.exists(self.kwargs['directory']) and len(os.listdir(self.kwargs['directory'])) > 0
                if url.endswith('.git'):
                    if not cache_exists:
                        subprocess.run([
                            'git', 'clone', '--depth', '1', url, self.kwargs['directory']
                        ], check=True)
                    else:
                        subprocess.run([
                            'git', 'pull'
                        ], cwd=self.kwargs['directory'], check=False)

                elif url.endswith('.zip'):
                    if not cache_exists:
                        zip_r = requests.get(url)
                        zip_mem = zipfile.ZipFile(io.BytesIO(zip_r.content))
                        if not os.path.exists(self.kwargs['directory']):
                            os.makedirs(self.kwargs['directory'])
                        print('extracting to {}'.format(self.kwargs['directory']))
                        zip_mem.extractall(self.kwargs['directory'])

                    deflate_dir(self.kwargs['directory'])

                else:
                    raise Exception('Unknown URL type: {}'.format(url))

                return self.kwargs['directory']

            else:
                raise Exception('Not enough information given to get/download CWD for SW_Repository')


        else:
            raise Exception('Cannot get_cwd for Deliverable of type_={}'.format(self.type_))

    def get_report_desc(self):
        """
        Describes the deliverable using HTML.
        """
        if self.type_ == 'SW_Repository':
            if self.kwargs['url']:
                return "Remote code and/or artifacts from <code>{}</code> cloned to local directory <code>{}</code>".format(
                    html.escape(self.kwargs['url']),
                    html.escape(self.kwargs['directory'])
                )

            elif self.kwargs['directory']:
                return "Local directory of code and/or artifacts: <code>{}</code>".format(html.escape(self.kwargs['directory']))

            else:
                raise Exception('Unknown type of SW_Repository')

        elif self.type_ == 'Phys_Item':
                return "Physical item: <code>{}</code>".format(
                    html.escape(self.kwargs['item_name'])
                )

        else:
            raise Exception('Cannot get_report_desc for Deliverable of type_={}'.format(self.type_))

# These constants are merely used as words/types in other systems (mostly for deliverables)
# Avoid using falsey values like "", 0, or [] because we often use None
# values as defaults and test if variables have been set with "if not X: raise Exception('must specify X')"
def SW_Application(archive_url=None, directory=None, app_executable_name=None):
    """Creates a deliverable of type SW_Application"""
    if not app_executable_name:
        raise Exception('All SW_Application deliverables must specify app_executable_name=')
    if (not archive_url) and (not directory):
        raise Exception('All SW_Application deliverables must specify either a archive_url= pointing to a download or a directory= pointing to deliverable files')    

    return Deliverable(
        type_='SW_Application',
        url=archive_url,
        directory=directory,
        app_executable_name=app_executable_name,
    )

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

def Phys_Item(item_name=None):
    """Creates a Deliverable which is a single physical item"""
    if not item_name:
        raise Exception('Phys_Item must have an item_name= specified!')

    return Deliverable(
        type_='Phys_Item',
        item_name=item_name,
    )


