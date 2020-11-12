
import subprocess
import threading
import os

class Task:
    def __init__(self, task_name, **kwargs):
        if not task_name:
            raise Exception('Task was not given a name!')
        self.project = None
        self.task_name = task_name
        self.kwargs = dict(kwargs)

    def set_project(self, project):
        self.project = project

    def evaluate(self):
        task_method_to_call = getattr(self, self.task_name)
        return task_method_to_call()

    # Now define all the various compile/launch/whatever methods
    def compile(self):
        if self.kwargs['build_system'] == 'make':
            p = subprocess.run(['make'], cwd=self.project.get_cwd())
            if p.returncode:
                return False # Something broke
            else:
                return True

        else:
            raise Exception('Unknown build_system for task "compile": {}'.format(self.kwargs['build_system']))

    def launch(self):
        f = self.kwargs['file']
        if not os.path.exists(f):
            f = os.path.join(self.project.get_cwd(), f)

        self.project.task_data['proc'] = subprocess.Popen([f] + self.kwargs['args'], cwd=self.project.get_cwd())
        self.project.task_data['proc_stdout'] = ""
        
        # Run thread to copy stdout into self.project.task_data['proc_stdout']
        def poll_proc():
            for stdout_line in iter(self.project.task_data['proc'].stdout.readline, ""):
                self.project.task_data['proc_stdout'] += stdout_line

        threading.Thread(target=poll_proc, args=())
        if self.project.task_data['proc']:
          return True
        else:
          return False

    def stdout_check(self):
        if self.kwargs['must_contain']:
          # Check if proc_stdout has must_contain in it
          if self.kwargs['case_insensitive']:
            return self.kwargs['must_contain'].lower() in self.project.task_data['proc_stdout'].lower()
          else:
            return self.kwargs['must_contain']in self.project.task_data['proc_stdout']

        else:
            raise Exception('stdout_check unimplemented given kwargs={}'.format(self.kwargs))

        return False


def Task_Compile(build_system=None):
    return Task('compile', build_system=build_system)

def Task_LaunchProgram(file=None, args=[]):
    return Task('launch', file=file, args=args)

def Task_StdoutCheck(must_contain=None, case_insensitive=False):
    return Task('stdout_check', must_contain=must_contain, case_insensitive=case_insensitive)



