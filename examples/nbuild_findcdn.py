
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
      name='findcdn identifies google.com as being hosted by Google',
      tests=[
        nb.Test(
          name='findcdn launches',
          task=nb.Task_LaunchProgram(
            file='python',
            args=['-m', 'findcdn', 'list', 'google.com'],
            cwd='src'
          )
        ),
        nb.Test(
          name='output contains "Google"',
          task=nb.Task_StdoutCheck(must_contain='Google', case_insensitive=False, delay_s=2, min_bytes=100)
        ),
        nb.Test(
          name='output contains "googlehosted.com"',
          task=nb.Task_StdoutCheck(must_contain='googlehosted.com', case_insensitive=False, delay_s=0, min_bytes=100)
        ),
      ]
    ),

    nb.Test(
      name='findcdn identifies apple.com as being hosted by Akamai',
      tests=[
        nb.Test(
          name='findcdn launches',
          task=nb.Task_LaunchProgram(
            file='python',
            args=['-m', 'findcdn', 'list', 'apple.com'],
            cwd='src'
          )
        ),
        nb.Test(
          name='output contains "Akamai"',
          task=nb.Task_StdoutCheck(must_contain='Akamai', case_insensitive=False, delay_s=2, min_bytes=100)
        ),
      ]
    ),

    nb.Test(
      name='findcdn identifies code.gov as being hosted by Cloudfront',
      tests=[
        nb.Test(
          name='findcdn launches',
          task=nb.Task_LaunchProgram(
            file='python',
            args=['-m', 'findcdn', 'list', 'code.gov'],
            cwd='src'
          )
        ),
        nb.Test(
          name='output contains "Cloudfront"',
          task=nb.Task_StdoutCheck(must_contain='Cloudfront', case_insensitive=False, delay_s=2, min_bytes=100)
        ),
      ]
    )


  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




