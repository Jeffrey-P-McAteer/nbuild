
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
      then='''
        the delivered spaceship will not be to-spec with the NCC-1701 ship we are trying to replicate.
        Cost will be unchanged, schedule will be unchanged. This is a qualitative risk.
      ''',
      probability=3,
      impact=5,
      mitigation=nb.Mitigation.Accept(),
    ),
    nb.Risk(
      name='Rocket launch price increases',
      if_='the price of commercial rocket launches increases by more than $1mil/per launch',
      then='''
        (cost) the project will be over-budget by $1mil/per remaining launch, with a maximum of $30mil (30 launches req. total).
        The schedule may be delayed by the amount of time it takes to secure funds if we cannot get more funding to cover new costs.
      ''',
      probability=2,
      impact=4,
      mitigation=nb.Mitigation.Control('''
        We will invest $5mil in a private space corporation and use our voting shares to vote against price increases.
        At the end of launches the $5mil investment will be liquidated to provide funds to finish the spaceship.
      '''),
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




