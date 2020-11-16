
import os

# python -m pip install --user nbuild
import nbuild as nb

this_dir = os.path.dirname(os.path.abspath(__file__))

p = nb.Project(
  name='Coordinate Systems Class Library',
  poc='Justin Strickland',
  description='''
    Library of classes representing various coordinate systems and providing the transformations between them.
    Coordinate systems represented are:
      East-North-Up (ENU)
      Downrange-Crossrange-Above (DCA)
      Latitude-Longitude-Altitude (LLA)
      Earth-Centered-Fixed (ECF)
      and Azimuth-Elevation-Range (AER).''',
  type_=nb.SW_Application,
  deliverable=nb.SW_Repository(url='https://github.com/nasa/Coordinate-systems-class-library.git', use_cache=True),
  tests=[
    
    nb.Test(name='Code compiles', task=nb.Task_Compile(build_system='unknown')),

    # This code is imposible to test because there is no build system.
    # Requiring contract writers to figure out a build system for a directory of
    # code is beyond the scope of nbuild.

  ]
)

# This actually begins the evaluation
p.evaluate()

p.write_reports_to(os.path.join(this_dir, 'reports'))

# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




