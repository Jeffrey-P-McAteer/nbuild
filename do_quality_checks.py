
import os
import subprocess

# This only exists b/c pylint requires it
# and by importing it we fail early when
# the user needs to install it.
#    python3 -m pip install --user astroid
import astroid


if __name__ == '__main__':
  
  subprocess.run([
    'pylint', 'nbuild'
  ], check=False)
