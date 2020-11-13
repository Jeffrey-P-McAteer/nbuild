
import os

# python -m pip install --user nbuild
import nbuild as nb

this_dir = os.path.dirname(os.path.abspath(__file__))

p = nb.Project(
  name='Project 01',
  poc='Jeffrey McAteer <jeffrey.p.mcateer@some-site.com>',
  description='P01 shows testing of an interactive program by a human operator',
  type_=nb.SW_Application,
  deliverable=nb.SW_Repository(directory=os.path.join(this_dir, 'proj01')),
  tests=[
    
    nb.Test(name='Code compiles', task=nb.Task_Compile(build_system='make')),

    nb.Test(
      name='non-interactive test',
      tests=[
        nb.Test(name='Executable launches', task=nb.Task_LaunchProgram(file='main.exe', args=['John Smith'])),
        nb.Test(name='App Greets User (non-interactive)', task=nb.Task_StdoutCheck(must_contain='hello john smith', case_insensitive=True)),

      ]
    ),

    nb.Test(
      name='interactive test',
      tests=[
        nb.Test(name='Executable launches', task=nb.Task_LaunchProgram(file='main.exe', interactive=True)),
        nb.Test(name='App asks for user name', task=nb.Task_StdoutCheck(must_contain='what is your name', case_insensitive=True)),
        nb.Test(
            name='Tester must record typed in username',
            task=nb.Task_TesterQuestion(question='What username did you type in?', save_as='user_name')
        ),
        nb.Test(name='App greets user', task=nb.Task_StdoutCheck(must_contain='hello {user_name}', case_insensitive=True)),

      ]
    ),

  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




