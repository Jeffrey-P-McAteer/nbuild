
import subprocess
import threading
import os
import time

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

        self.project.task_data['proc'] = subprocess.Popen(
            [f] + self.kwargs['args'],
            cwd=self.project.get_cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0, # unbuffered
        )
        self.project.task_data['proc_stdout'] = ""

        # Run thread to copy stdout into self.project.task_data['proc_stdout']
        def poll_proc():
            p = self.project.task_data['proc']
            while True:
                out = p.stdout.read(1)
                is_empty = (out == '' or out == b'' or len(out) < 1)
                if is_empty and p.poll() != None:
                    break
                if not is_empty:
                    # To/Do this will break pretty badly if we have multibyte utf-8 characters
                    self.project.task_data['proc_stdout'] += out.decode('utf-8')

        t = threading.Thread(target=poll_proc, args=())
        t.start()
        
        # Pause for 1/4 second to let process begin (lots of tests will expect some stdout)
        time.sleep(0.25)

        if self.project.task_data['proc']:
          return True
        else:
          return False

    def stdout_check(self):
        if self.kwargs['must_contain']:
          # Check if proc_stdout has must_contain in it
          # print('proc_stdout={}'.format(self.project.task_data['proc_stdout']))
          must_contain = self.kwargs['must_contain']

          if '{' in must_contain and '}' in must_contain:
            # Pass all project.task_data variables through for replacement
            print('self.project.task_data=', self.project.task_data)
            must_contain = must_contain.format( **self.project.task_data ) # ** unpacks dict into .format()'s **kwargs

          if self.kwargs['case_insensitive']:
            return must_contain.lower() in self.project.task_data['proc_stdout'].lower()
          else:
            return must_contain in self.project.task_data['proc_stdout']

        else:
            raise Exception('stdout_check unimplemented given kwargs={}'.format(self.kwargs))

        return False

    def tester_question(self):
        self.project.task_data[ self.kwargs['save_as'] ] = input(self.kwargs['question']+' ')
        return True


def Task_Compile(build_system=None):
    return Task('compile', build_system=build_system)

def Task_LaunchProgram(file=None, args=[]):
    return Task('launch', file=file, args=args)

def Task_StdoutCheck(must_contain=None, case_insensitive=False):
    return Task('stdout_check', must_contain=must_contain, case_insensitive=case_insensitive)

def Task_TesterQuestion(question=None, save_as='last_resp'):
    return Task('tester_question', question=question, save_as=save_as)

