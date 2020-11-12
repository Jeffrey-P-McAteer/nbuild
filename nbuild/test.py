
"""

"""


import os
import subprocess
import platform
import shutil

# from nbuild.util import ask_yn_q

class Test:
    def __init__(self, name=None, description="", task=None, tests=[]):
        if not name:
            raise Exception('Error: Test was not given a name!')
        if (not task) and (not tests):
            raise Exception('Error: Test was not given a task or sub-tests; either a task or a list of tests must be given.')
        self.name = name
        self.description = description
        self.task = task
        self.tests = tests
        # Data set by the project during initialization
        self.project = None
        # Data set during testing
        self.passed = False

    def set_project(self, project):
        self.project = project
        if self.task:
            self.task.set_project(project)
        elif self.tests:
            for t in self.tests:
                t.set_project(project)

    def evaluate(self):
        if self.task:
            self.passed = self.task.evaluate()
        elif self.tests:
            all_passed = True
            for t in self.tests:
                p = t.evaluate()
                if not p:
                    all_passed = False
            # If even a single sub-test is wrong, the entire group is wrong
            self.passed = all_passed

        return self.passed


