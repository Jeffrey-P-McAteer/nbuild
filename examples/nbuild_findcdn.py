
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
  risks=[
    nb.Risk(
      name='CDN identification data is unavailable',
      if_='CDN ip range, host headers, or other identification data is unknown to us',
      then='For a given set of domains CDN identification will be impossible',
      probability=4,
      impact=1,
      mitigation=nb.Mitigation.Accept(),
    ),
    nb.Risk(
      name='random risk',
      if_='something happens',
      then='another thing will occur',
      probability=3,
      impact=2,
      mitigation=nb.Mitigation.Transfer('James Smith <jsmith@example.com>, specifically project X will handle this risk if it occurs.'),
    ),
    nb.Risk(
      name='random risk 2',
      if_='something happens',
      then='another thing will occur',
      probability=5,
      impact=1,
      mitigation=nb.Mitigation.Control('We will bolt on 1/2 inch steel plates which will make that side of the machine heavier and less likely to tip over.')
    ),
    nb.Risk(
      name='random risk 3',
      if_='something happens',
      then='another thing will occur',
      probability=1,
      impact=5
    ),
    nb.Risk(
      name='dupe of random risk 3',
      if_='something happens',
      then='another thing will occur',
      probability=1,
      impact=5
    ),
    nb.Risk(
      name='BIG RISK',
      if_='something happens',
      then='another thing will occur',
      probability=5,
      impact=5
    ),
  ],
  tests=[

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




