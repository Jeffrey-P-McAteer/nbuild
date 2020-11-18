
import os

# python -m pip install --user nbuild
import nbuild as nb

this_dir = os.path.dirname(os.path.abspath(__file__))

p = nb.Project(
  name='Spaceship Project',
  poc='Jeffrey McAteer <nobody@example.org>',
  description='''
    The spaceship project aims to build a real-life replica of the starship from Star Trek.
    Specifically the NCC-1701 will be used as a target model (see https://en.wikipedia.org/wiki/USS_Enterprise_(NCC-1701) )
  ''',
  type_=nb.SW_Application,
  deliverable=nb.Phys_Item(
    item_name='Spaceship',
  ),
  risks=[
    nb.Risk(
      name='faster-than-light travel',
      if_='faster-than-light travel is determined to be impossible',
      then='the delivered spaceship will not be to-spec with the NCC-1701 ship we are trying to replicate',
      probability=3,
      impact=5,
      mitigation=nb.Mitigation.Accept(),
    ),
  ],
  tests=[

  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




