
"""
The project module holds the Project class
and is responsible for modeling an entire project/contract/effort
"""

import os
import platform
import subprocess
import time
import math

from nbuild import report

class Project:
    """
    The Project class is responsible for modeling an entire project/contract/effort
    """
    def __init__(self,
                 name=None,
                 poc='',
                 description='',
                 type_=None,
                 deliverable=None,
                 risks=None,
                 tests=None
                 ):
        # First check args (fatal errors)
        if not name:
            raise Exception('Error: Project was not given a name!')
        if not type_:
            raise Exception('Error: Project was not given a type!')
        if not deliverable:
            raise Exception('Error: Project was not given a deliverable!')
        if risks is None:
            raise Exception('Error: Project was not given any risks!')
        if tests is None:
            raise Exception('Error: Project was not given any tests!')
        
        # Warnings are not blockers but things that are missing/should be improved in the project description;
        # e.g. not mentioning cost impact in a risk.
        self.warnings = []

        # Check args (non-fatal warnings)
        if not poc:
            w = 'WARNING: no point of contact given for project: {}'.format(name)
            print(w)
            self.warnings.append(w)
        
        if len(tests) < 1:
            w = 'WARNING: no tests given for project: {}'.format(name)
            print(w)
            self.warnings.append(w)

        if len(risks) < 1:
            w = 'WARNING: no risks given for project: {}'.format(name)
            print(w)
            self.warnings.append(w)

        # Then assign state data
        self.name = name.strip()
        self.poc = poc.strip()
        # Descriptions are modified such that only a single space is used instead of
        # multiple spaces and newlines are removed.
        # This allows project authors to indent descriptions without having those indentations
        # move words around in the report.
        self.description = (' '.join(description.split())).strip()
        self.type_ = type_
        self.deliverable = deliverable
        self.risks = risks
        self.tests = tests

        # and initialize state used during eval/reporting stages
        self.reports = []
        self.task_data = {} # tasks may assign whatever key/value data they want here
        self.evaluated = False
        self.evaluation_duration_s = 0

        for t in self.tests:
            t.set_project(self)

        for t in self.risks:
            t.set_project(self)

    def evaluate(self):
        """Runs all tests and test tasks in the project"""
        if self.evaluated:
            print("Warning, evaluating {} twice...".format(self.name))

        eval_begin_s = time.time()
        for t in self.tests:
            t.evaluate()

        self.evaluated = True
        self.evaluation_duration_s = math.ceil(time.time() - eval_begin_s)

    def get_cwd(self):
        """
        Asks the deliverable for it's CWD.
        This may be a specified directory or the deliverable may download data, extract it, and return the extracted directory.
        Some deliverables, such as goods + services, will raise an exception if asked for their CWD.
        """
        return self.deliverable.get_cwd()

    def get_warning_lines(self):
        """Returns warnings joined by a newline"""
        return (''+os.linesep).join(self.warnings)

    def write_reports_to(self, directory='.'):
        """
        Generates reports after evaluation and writes them to the specified directory, defaulting to "."
        """
        if not self.evaluated:
            raise Exception('Cannot write reports for an un-evaluated project, call .evaluate() first!')

        if not os.path.exists(directory):
            os.makedirs(directory)
        report.write_reports_to(self, directory)

    def open_reports(self):
        """
        Must be called after write_reports_to has been called.
        Opens all report files in their default programs, for example
        Chrome will usually open .html files and Adobe products will usually open .pdf files.
        """
        for filepath in self.reports:
            if platform.system() == 'Darwin':
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':
                # pylint: disable=no-member
                os.startfile(filepath)
            else:
                subprocess.call(('xdg-open', filepath))

