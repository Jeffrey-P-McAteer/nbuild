
import os
import sys
import subprocess
import platform
import tempfile
import shutil

from nbuild.util import ask_yn_q

class BuildSystem:
  def __init__(self, _type="none", *args, **kwargs):
    self._type = _type
    self.project = None
    self.args = args
    self.kwargs = kwargs

  def build(self, project=None):
    # Default to self.project
    if self.project and not project:
      project = self.project

    if self._type == "make":
      subprocess.run([
        'make', *self.args
      ], cwd=project.get_cwd(), check=True)

    elif self._type == "npm":
      subprocess.run([
        'npm', 'install'
      ], cwd=project.get_cwd(), check=True)

      subprocess.run([
        'npm', *self.kwargs['cmds']
      ], cwd=project.get_cwd(), check=True)
    
    elif self._type == "physical":
      
      print("Please ensure the following items are available at the test site:")
      for item in project.deliverables_in.items:
        print("> {}".format(item))
      
      if ask_yn_q('Are all items available?'):
        for step in [x for x in self.kwargs['steps']]:
          print('')
          if step.lower().startswith('q:'):
            response = ask_yn_q(step[2:])
            if not response:
              print('A setup step cannot be completed, test is finished')
              break
          else:
            print('> {}'.format(step))
            response = ask_yn_q('Type "yes" when step completed, or "no" if step cannot be completed.')
            if not response:
              print('A setup step cannot be completed, test is finished')
      else:
        print('An item is missing, test is finished.')


    elif self._type == "none":
      pass
    else:
      raise Exception("Unknown build type '{}'".format(self._type))

