
import os

# python -m pip install --user nbuild
import nbuild as nb

this_dir = os.path.dirname(os.path.abspath(__file__))

p = nb.Project(
  name='NASA WorldWind (Java)',
  poc='Jeffrey McAteer <jeffrey.p.mcateer@some-site.com>',
  description='NASA WorldWind comes with demo apps, one of which we will test.',
  type_=nb.SW_Application,
  deliverable=nb.SW_Repository(url='https://github.com/NASAWorldWind/WorldWindJava.git'),
  tests=[
    
    nb.Test(name='Code compiles', task=nb.Task_Compile(build_system='ant')),

    nb.Test(
      name='interactive test',
      tests=[
        nb.Test(
          name='Executable launches',
          task=nb.Task_LaunchProgram(
            file='java',
            args=[
              '-cp', 'build/classes/:gdal.jar:gluegen-rt.jar:jogl-all.jar',
              'gov.nasa.worldwindx.examples.SimplestPossibleExample'
            ],
            interactive=True
          )
        ),

        nb.Test(
            name='Globe UI appears',
            task=nb.Task_TesterQuestion(question='Did a window with a globe open?')
        ),


      ]
    ),

  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




