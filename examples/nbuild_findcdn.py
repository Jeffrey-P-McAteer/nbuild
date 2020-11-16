
import os

# python -m pip install --user nbuild
import nbuild as nb

this_dir = os.path.dirname(os.path.abspath(__file__))

p = nb.Project(
  name='findcdn',
  poc='Nick M. (https://github.com/mcdonnnj)',
  description='findCDN is a tool created to help accurately identify what CDN a domain is using.',
  type_=nb.SW_Application,
  deliverable=nb.SW_Repository(url='https://github.com/cisagov/findcdn.git', use_cache=True),
  tests=[
    
    # nb.Test(
    #   name='findcdn dependencies can be installed on test machine',
    #   task=nb.Task_LaunchProgram(
    #     file='python',
    #     args=['-m', 'pip', 'install', '--user', '--requirement', 'requirements-test.txt']
    #   )
    # ),

    # nb.Test(
    #   name='findcdn launches',
    #   task=nb.Task_LaunchProgram(file='findcdn', args=['list', 'github.com'])
    # ),


    nb.Test(
      name='findcdn launches',
      task=nb.Task_LaunchProgram(
        file='python',
        args=['-m', 'findcdn', 'list', 'github.com'],
        cwd='src'
      )
    ),

    nb.Test(
      name='findcdn reports github.com as being hosted on Azure',
      task=nb.Task_StdoutCheck(must_contain='azure', case_insensitive=True, delay_s=2, min_bytes=100)
    ),

  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




