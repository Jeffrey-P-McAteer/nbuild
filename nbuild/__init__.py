
import os
import sys
import subprocess
import platform
import tempfile
import shutil

from nbuild.project import Project
from nbuild.deliverable import Deliverable
from nbuild.build import BuildSystem
from nbuild.test import TestSystem

# Deliverable constructors
def src_directory(path):
  return Deliverable(_type="directory", path=path)

def src_file(path):
  return Deliverable(_type="file", path=path)

def executable(path):
  return Deliverable(_type="file", path=path)

def git_repository(url, git_dir=None):
  return Deliverable(_type="git", url=url, git_dir=git_dir)

def physical_items(*items):
  return Deliverable(_type="items", items=list(items))

# Build system constructors
def make(*args):
  targets = [x for x in args]
  return BuildSystem(_type="make", targets=targets)

def npm_build(*args):
  cmds = [x for x in args]
  return BuildSystem(_type="npm", cmds=cmds)

def physical_prep(*steps):
  steps = [x for x in steps]
  return BuildSystem(_type="physical", steps=steps)


# Test system constructors
def execute(*args):
  return TestSystem(
    _type="execute",
    exec_args=list(args)
  )

def npm_test(*args):
  cmds = [x for x in args]
  return TestSystem(_type="npm", cmds=cmds).default_npm()

def physical_test(*steps):
  steps = [x for x in steps]
  return TestSystem(_type="physical", steps=steps).default_physical()



