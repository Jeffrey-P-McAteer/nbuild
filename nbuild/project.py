
import os
import platform
import subprocess

from nbuild import report

class Project:
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

      for t in self.tests:
          t.set_project(self)

  def evaluate(self):
      for t in self.tests:
          pass

  def write_reports_to(self, directory='.'):
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

