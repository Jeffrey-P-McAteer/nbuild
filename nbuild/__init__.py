
import os
import sys
import subprocess
import platform
import tempfile
import shutil

def ask_yn_q(question):
  question = question+' '
  resp = input(question).strip().lower()
  while resp[0] != 'y' and resp[0] != 'n':
    print("Please answer 'yes' or 'no' ('y' and 'n' are also accepted)")
    resp = input(question).strip().lower()
  # True if 'y' False if 'n'
  return resp[0] == 'y'

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
    self.build_system.project = self

    if deliverables_out == None:
      deliverables_out = self.deliverables_in
    if not isinstance(deliverables_out, (Deliverable)):
      raise Exception("deliverables_out must be a Deliverable")
    self.deliverables_out = deliverables_out

    if not isinstance(test_system, (TestSystem)):
      raise Exception("test_system must be a TestSystem")
    self.test_system = test_system
    self.test_system.project = self
    

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
    self.project = None
    # Holds Test objects
    self.tests = []
    # Holds any generated report files
    self.reports = []
    # These are _type-dependent flags
    self.execute_stdout = ""
    self.execute_process_crashed = False
    self.execute_process_crashed_msg = None
    self.physical_test_notes = ""
    

  def with_stdout(self, description, task):
    if self._type != "execute":
      raise Exception("Cannot call with_stdout unless task type is 'execute'")
    self.tests.append(Test(
      description=description,
      task=task
    ));
    return self

  def default_npm(self):
    if self._type != "npm":
      raise Exception("Cannot call default_npm unless task type is 'npm'")
    def inner_npm():
      
      subprocess.run([
        'npm', *self.kwargs['cmds']
      ], cwd=self.project.get_cwd(), check=True)

      return True

    self.tests.append(Test(
      description='NPM Test; see the test report generated below for details.',
      task=inner_npm
    ));

    return self

  def default_physical(self):
    if self._type != "physical":
      raise Exception("Cannot call default_physical unless task type is 'physical'")
    
    def inner_physical(step):
      
      print('')
      if step.lower().startswith('q:'):
        return ask_yn_q(step[2:].strip())
        
      else:
        print('> {}'.format(step))
        return ask_yn_q('Type "yes" when step completed, or "no" if step cannot be completed.')

      return False
        
    for step in [x for x in self.kwargs['steps']]:
      self.tests.append(Test(
        description=step,
        task=(lambda istep: lambda: inner_physical(istep))(step) # 1 level of indirection so we save THIS iteration's step value
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
    if self._type == "execute":
      for t in self.tests:
        passed = t.test(self.execute_stdout)

    elif self._type == "npm":
      for t in self.tests:
        passed = t.test()

    elif self._type == "physical":
      for t in self.tests:
        passed = t.test()
      self.physical_test_notes = input('Write any additional notes here, typing enter when complete: ')

    else:
      raise Exception("Unknown testing procedure for TestSystem._type = {}".format(self._type))

  def write_reports_to(self, project, directory):
    test_rep_path = os.path.join(directory, 'nbuild_test_report.html')
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
      elif self.execute_stdout:
        closing_remarks = "<p>Program Output:</p><pre>{output}</pre>".format(output=self.execute_stdout)

      elif self._type == "npm":
        test_res_dir = os.path.join(self.project.get_cwd(), 'build', 'test-results')
        if os.path.exists(test_res_dir):
          # Grab first .html file, copy to "directory", then add <iframe> pointint to it
          copied_report_prefix = 'nbuild_cp_'
          first_report_f = None
          for report_f in os.listdir(test_res_dir):
            if report_f.endswith('.html'):
              first_report_f = copied_report_prefix+report_f
              shutil.copy(os.path.join(test_res_dir, report_f), os.path.join(directory, first_report_f))
              break;

          if first_report_f:
            closing_remarks = '<iframe src="{first_report_f}" width="100%" height="900pt" style="border: 1px solid black;"></iframe>'.format(first_report_f=first_report_f)

      elif self._type == "physical":
        closing_remarks = "<p>Additional test comments:</p><pre>{notes}</pre>".format(notes=self.physical_test_notes)

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
pre {{
  overflow-x: auto;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
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



