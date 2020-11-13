
"""
The project module holds the Project class
and is responsible for modeling an entire project/contract/effort
"""

import os
import platform
import subprocess

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
                 tests=None
                 ):
        # First check args (fatal errors)
        if not name:
            raise Exception('Error: Project was not given a name!')
        if not type_:
            raise Exception('Error: Project was not given a type!')
        if not deliverable:
            raise Exception('Error: Project was not given a deliverable!')
        if not tests:
            raise Exception('Error: Project was not given any tests!')
        # Check args (non-fatal warnings)
        if not poc:
            print('Warning: no point of contact given for project: {}'.format(name))
        
        # Then assign state data
        self.name = name
        self.poc = poc
        self.description = description
        self.type_ = type_
        self.deliverable = deliverable
        self.tests = tests

        # and initialize state used during eval/reporting stages
        self.reports = []
        self.task_data = {} # tasks may assign whatever key/value data they want here

        for t in self.tests:
            t.set_project(self)

    def evaluate(self):
        """Runs all tests and test tasks in the project"""
        for t in self.tests:
            t.evaluate()

    def get_cwd(self):
        """
        Asks the deliverable for it's CWD.
        This may be a specified directory or the deliverable may download data, extract it, and return the extracted directory.
        Some deliverables, such as goods + services, will raise an exception if asked for their CWD.
        """
        return self.deliverable.get_cwd()

    def write_reports_to(self, directory='.'):
        """
        Generates reports after evaluation and writes them to the specified directory, defaulting to "."
        """
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

