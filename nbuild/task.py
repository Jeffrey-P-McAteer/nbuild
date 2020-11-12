

class Task:
    def __init__(self):
        self.project = None
        

    def set_project(self, project):
          self.project = project


def Task_Compile(build_system=None):
    return Task()

def Task_LaunchProgram(file=None, args=[]):
    return Task()

def Task_StdoutCheck(must_contain=None, case_insensitive=False):
    return Task()



