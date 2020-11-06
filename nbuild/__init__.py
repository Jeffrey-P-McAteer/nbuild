
import os
import sys
import subprocess
import platform

class Project:
  def __init__(
    self,
    name="Unnamed Project",
    deliverables_in=None,
    build_system=None,
    deliverables_out=None,
    test_system=None,

  ):
    self.name = name
    
    if not isinstance(deliverables_in, (Deliverable)):
      raise Exception("deliverables_in must be a Deliverable")
    self.deliverables_in = deliverables_in

    if not isinstance(build_system, (BuildSystem)):
      raise Exception("build_system must be a BuildSystem")
    self.build_system = build_system

    if deliverables_out == None:
      deliverables_out = self.deliverables_in
    if not isinstance(deliverables_out, (Deliverable)):
      raise Exception("deliverables_out must be a Deliverable")
    self.deliverables_out = deliverables_out

    if not isinstance(test_system, (TestSystem)):
      raise Exception("test_system must be a TestSystem")
    self.test_system = test_system
    

  def build(self):
    self.build_system.build(self)

  def test(self):
    self.test_system.test(self)
  
  def write_reports_to(self, directory):
    if not os.path.exists(directory):
      os.makedirs(directory)

    self.test_system.write_reports_to(self, directory)

  def open_reports(self):
    self.test_system.open_reports()

  # Utilities for build + test systems to use,
  # answers common questions about projects.

  def get_cwd(self):
    return self.deliverables_in.get_cwd()

  

class Deliverable:
  def __init__(self, _type="file", path="", url=""):
    self._type = _type
    self.path = path
    self.url = url

  def get_cwd(self):
    if not self._type == "directory":
      raise Exception("get_cwd only makes sense for Deliverable of type 'directory'")
    return self.path

class BuildSystem:
  def __init__(self, _type="make", *args, **kwargs):
    self._type = _type
    self.args = args
    self.kwargs = kwargs

  def build(self, project):
    if self._type == "make":
      subprocess.run([
        'make', *self.args
      ], cwd=project.get_cwd(), check=True)
    else:
      raise Exception("Unknown build type '{}'".format(self._type))

class Test:
  def no_task_task():
    raise Exception("No task specified!")

  def __init__(self, description="No Description", task=no_task_task):
    self.description = description
    self.task = task
    self.passed = False

  def test(self, *args):
    p = self.task(*args)
    if not isinstance(p, (bool)):
      raise Exception("test tasks MUST return a boolean (True or False). Good examples may be a lambda that returns 'x == 5' or 'output.startswith(\"completed\")'")
    self.passed = p


class TestSystem:
  def __init__(self, _type="execute", *args, **kwargs):
    self._type = _type
    self.args = args
    self.kwargs = kwargs
    # Holds Test objects
    self.tests = []
    # Holds any generated report files
    self.reports = []
    # These are _type-dependent flags
    self.execute_stdout = ""
    self.execute_process_crashed = False
    self.execute_process_crashed_msg = None

  def with_stdout(self, description, task):
    if self._type != "execute":
      raise Exception("Cannot call with_stdout unless task type is 'execute'")
    self.tests.append(Test(
      description=description,
      task=task
    ));
    return self

  def run_pretest_tasks(self, project):
    if self._type == "execute":
      try:
        self.execute_stdout = subprocess.run(
          self.kwargs['exec_args'],
          cwd=project.get_cwd(),
          check=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT
        ).stdout.decode('utf-8')
      except subprocess.CalledProcessError as e:
        self.execute_process_crashed = True
        self.execute_process_crashed_msg = e.output.decode('utf-8') + os.linesep + os.linesep + str(e)


  def test(self, project):
    self.run_pretest_tasks(project)
    if len(self.tests) < 1:
      raise Exception("No tests specified!")
    for t in self.tests:
      passed = t.test(self.execute_stdout)

  def write_reports_to(self, project, directory):
    test_rep_path = os.path.join(directory, 'test_report.html')
    with open(test_rep_path, 'w') as test_rep:
      # test_table is a bunch of <tr> rows with <td> columns
      test_table = ""
      for t in self.tests:
        test_table += '<tr><td class="{_class}">{passed}</td><td>{description}</td></tr>'.format(
          _class='passed' if t.passed else 'failed',
          passed='Passed' if t.passed else 'Failed',
          description=t.description
        )

      closing_remarks = ""
      if self.execute_process_crashed:
        closing_remarks = "<p>The program crashed during execution. Output is shown below.</p><pre>{output}</pre>".format(
          output=self.execute_process_crashed_msg
        )

      test_rep.write("""<DOCTYPE html>
<html lang="en">
  <head>
    <title>{name} Test Report</title>
    <style>
table, th, td {{
  border: 1px solid black;
  border-collapse: collapse;
}}
th, td {{
  padding: 4pt 8pt;
}}
.passed {{
  background-color: #90ee90; /* light green */
}}
.failed {{
  background-color: #ffcccb; /* light red */
}}
    </style>
  </head>
  <body>
    <h1>{name} Test Report</h1>
     <table>
      <tr>
        <th>Status</th>
        <th>Description</th>
      </tr>
      {test_table}
    </table>
    {closing_remarks}
  </body>
</html>
""".format(
        name=project.name,
        test_table=test_table,
        closing_remarks=closing_remarks
      ))

    self.reports.append(test_rep_path)

  def open_reports(self):
    for filepath in self.reports:
      if platform.system() == 'Darwin':
          subprocess.call(('open', filepath))
      elif platform.system() == 'Windows':
          os.startfile(filepath)
      else:
          subprocess.call(('xdg-open', filepath))


# Deliverable constructors
def src_directory(path):
  return Deliverable(_type="directory", path=path)

def src_file(path):
  return Deliverable(_type="file", path=path)

def executable(path):
  return Deliverable(_type="file", path=path)

# Build system constructors
def make(targets=[]):
  return BuildSystem(_type="make", targets=targets)

# Test system constructors
def execute(*args):
  return TestSystem(
    _type="execute",
    exec_args=list(args)
  )




