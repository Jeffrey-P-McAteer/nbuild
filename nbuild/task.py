
import subprocess
import threading
import os
import sys
import time
import traceback

from multiprocessing.shared_memory import SharedMemory

def SharedMemoryCreator(name=None, size=None):
  try:
    return SharedMemory(name=name, size=size, create=True)
  except Exception as e:
    pass
  return SharedMemory(name=name, size=size, create=False)

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

        cmd = [f] + self.kwargs['args']
        if self.kwargs['interactive']:
          # OS-specific wrappers which in turn run [cmd]
          
          # We also call "python task.py [cmd]" to copy stdout
          # back to this process.
          cmd = [sys.executable, os.path.abspath(__file__)] + cmd

          if os.name == 'nt':
            cmd = ['start', '/wait'] + [ ' '.join(cmd) ]
          else:
            term = os.environ['TERM']
            if 'kitty' in term:
              cmd = ['kitty', '-e'] + cmd
            elif 'termite' in term:
              cmd = ['termite', '-e'] + [ ' '.join(cmd) ]
            else:
              raise Exception('Unknown GUI terminal for $TERM={}'.format(term))

        self.project.task_data['proc'] = subprocess.Popen(
            cmd,
            cwd=self.project.get_cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0, # unbuffered
        )
        self.project.task_data['proc_stdout'] = ""

        if self.kwargs['interactive']:
          def poll_shmem():
            sm = SharedMemoryCreator(name="nbuild_task", size=4096)
            while True:
              # Just copy all non-\0 characters out over and over, replacing with \0 once read
              for i in range(0, 4096):
                if sm.buf[i]:
                  self.project.task_data['proc_stdout'] += chr(sm.buf[i])
                  sm.buf[i] = 0

              # Check if process exited; if so we also exit
              if self.project.task_data['proc'].poll() != None:
                break

            sm.close()


          t = threading.Thread(target=poll_shmem, args=())
          t.start()

        else:
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

def Task_LaunchProgram(file=None, args=[], interactive=False):
    return Task('launch', file=file, args=args, interactive=interactive)

def Task_StdoutCheck(must_contain=None, case_insensitive=False):
    return Task('stdout_check', must_contain=must_contain, case_insensitive=case_insensitive)

def Task_TesterQuestion(question=None, save_as='last_resp'):
    return Task('tester_question', question=question, save_as=save_as)


# task.py also has this small program which wraps a given command and
# executes it, forwarding stdout to the parent process using shared memory.
# This is used to record program output when opening in a new GUI window for
# test operators to manipulate.

if __name__ == '__main__':
    cmd = sys.argv[1:]
    
    sm = None
    try:
      sm = SharedMemoryCreator(name="nbuild_task", size=4096)

      p = subprocess.Popen(
          cmd,
          #cwd=self.project.get_cwd(), # CWD must be set in task.launch (which it is)
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          bufsize=0, # unbuffered
      )

      # Write stdout to buffer, wrapping around + blocking if the next char is not '\0'
      next_free_i = 0;
      for i in range(0, 4096):
        sm.buf[i] = 0

      while True:
        out = p.stdout.read(1)
        is_empty = (out == '' or out == b'' or len(out) < 1)
        if is_empty and p.poll() != None:
            break
        if not is_empty:
            
            # Write all bytes read to stdout
            sys.stdout.buffer.write(out)
            sys.stdout.flush()

            # Write all bytes read to shared mem
            for b in out:
              # Wait until next free char is read
              while sm.buf[next_free_i] != 0:
                time.sleep(0.01)
              sm.buf[next_free_i] = b
              if next_free_i >= 4095:
                next_free_i = 0
                # Just a safety pause; ideally the reader would read everything before we roll around.
                time.sleep(0.01)
              else:
                next_free_i += 1

      sm.close()

    except Exception as e:
      traceback.print_exc()
      time.sleep(10) # Usually this is in a new console, give debugers some time to read errors

    if sm:
      sm.close()




