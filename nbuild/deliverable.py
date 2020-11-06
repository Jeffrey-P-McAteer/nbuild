
import os
import sys
import subprocess
import platform
import tempfile
import shutil

class Deliverable:
  def __init__(self, _type="file", path="", url="", git_dir=None, items=None):
    self._type = _type
    self.path = path
    self.url = url
    # Type-specific data
    self.git_dir = git_dir
    self.git_dir_obj = None
    self.items = items

  def get_cwd(self):
    if self._type == "git":
      if self.git_dir and os.path.exists(self.git_dir):
        return self.git_dir

      # Do a clone and return that
      if not self.git_dir:
        self.git_dir_obj = tempfile.TemporaryDirectory(suffix=''.join([x for x in self.url if x.isalnum()]))
        self.git_dir = self.git_dir_obj.name

      subprocess.run([
        'git', 'clone', self.url, self.git_dir
      ], check=True)

      return self.git_dir

    if not self._type == "directory":
      raise Exception("get_cwd only makes sense for Deliverable of type 'directory'")
    return self.path

