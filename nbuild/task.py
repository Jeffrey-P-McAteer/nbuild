
"""
The task module contains the Task class.
It also may be run standalone to capture
stdout from a process and send it to a shared memory buffer.
"""

import subprocess
import threading
import os
import sys
import time
import traceback

from multiprocessing.shared_memory import SharedMemory

def SharedMemoryCreator(name=None, size=None):
    """
    Wraps the multiprocessing.shared_memory.SharedMemory constructor to create the region
    of memory if it does not exist, otherwise re-use an existing region with the same name.
    """
    try:
        return SharedMemory(name=name, size=size, create=True)
    except: # pylint: disable=bare-except
        pass
    return SharedMemory(name=name, size=size, create=False)

class Task:
    """
    The Task class represents some step the tester
    needs to take. In many cases these steps may
    be automated (eg builds, downloads, some button pushing).
    Task instances should be created by calling the Task_* methods below.
    """
    def __init__(self, task_name, **kwargs):
        if not task_name:
            raise Exception('Task was not given a name!')
        self.project = None
        self.task_name = task_name
        self.kwargs = dict(kwargs)

    def set_project(self, project):
        """Assigns the project to be used when the task is evaluated (if CWD or shared data is needed)"""
        self.project = project

    def evaluate(self):
        """
        Executes a method and returns True/False if the task was successful.
        Some tasks may always result in a success but record metadata to the project (eg for qualitative records)
        """
        task_method_to_call = getattr(self, self.task_name)
        return task_method_to_call()

    def get_report_desc(self, name="", description=""):
        """
        Returns a description for this task, including any operator responses to questions
        """
        if self.task_name == 'tester_question':
            return '<details><summary>{name}</summary>Q: {question}<br>A: {answer}</details> '.format(
                name=name,
                question=self.kwargs['question'],
                answer=self.project.task_data[ self.kwargs['save_as'] ],
            )
        else:
            if name:
                return name
            if description:
                return description
            raise Exception('no name/description passed to Task.get_report_desc and unhandled self.task_name={}'.format(self.task_name))


    # Now define all the various compile/launch/whatever methods
    def compile(self): # pylint: disable=missing-function-docstring
        success = False
        if self.kwargs['build_system'] == 'make':
            p = subprocess.run(['make'], cwd=self.project.get_cwd()) # pylint: disable=subprocess-run-check
            if p.returncode:
                success = False # Something broke
            else:
                success = True

        elif self.kwargs['build_system'] == 'ant':
            p = subprocess.run(['ant'], cwd=self.project.get_cwd()) # pylint: disable=subprocess-run-check
            if p.returncode:
                success = False # Something broke
            else:
                success = True

        else:
            raise Exception('Unknown build_system for task "compile": {}'.format(self.kwargs['build_system']))
        return success

    def launch(self): # pylint: disable=missing-function-docstring
        f = self.kwargs['file']
        if not os.path.exists(f) and os.path.exists(os.path.join(self.project.get_cwd(), f)):
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
                    if self.project.task_data['proc'].poll() is not None:
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
                    if is_empty and p.poll() is not None:
                        break
                    if not is_empty:
                        # To/Do this will break pretty badly if we have multibyte utf-8 characters
                        self.project.task_data['proc_stdout'] += out.decode('utf-8')

            t = threading.Thread(target=poll_proc, args=())
            t.start()
        
        # Pause for 1/4 second to let process begin (lots of tests will expect some stdout)
        time.sleep(0.25)

        return bool(self.project.task_data['proc']) # true if process launched, otherwise maybe false

    def stdout_check(self): # pylint: disable=missing-function-docstring
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

    def tester_question(self): # pylint: disable=missing-function-docstring
        self.project.task_data[ self.kwargs['save_as'] ] = input(self.kwargs['question']+' ')
        return True


def Task_Compile(build_system=None):
    """Creates a Task which can compile code"""
    return Task('compile', build_system=build_system)

def Task_LaunchProgram(file=None, args=None, interactive=False):
    """Creates a Task which executes deliverables"""
    if args is None:
        args = []
    return Task('launch', file=file, args=args, interactive=interactive)

def Task_StdoutCheck(must_contain=None, case_insensitive=False):
    """Creates a Task which polls a previously launched program's output and checks it for given values"""
    return Task('stdout_check', must_contain=must_contain, case_insensitive=case_insensitive)

def Task_TesterQuestion(question=None, save_as='last_resp'):
    """Creates a Task which prompts the tester to enter some information which is saved in project.task_data"""
    return Task('tester_question', question=question, save_as=save_as)


def main():
    """
    task.py also has this small program which wraps a given command and
    executes it, forwarding stdout to the parent process using shared memory.
    This is used to record program output when opening in a new GUI window for
    test operators to manipulate.
    """
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
        next_free_i = 0
        for i in range(0, 4096):
            sm.buf[i] = 0

        while True:
            out = p.stdout.read(1)
            is_empty = (out == '' or out == b'' or len(out) < 1)
            if is_empty and p.poll() is not None:
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

    except Exception as e: # pylint: disable=broad-except,unused-variable
        traceback.print_exc()
        time.sleep(10) # Usually this is in a new console, give debugers some time to read errors

    if sm:
        sm.close()

if __name__ == '__main__':
    main()

