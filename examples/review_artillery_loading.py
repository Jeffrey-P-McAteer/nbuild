
import os

# Import nbuild; this requires nbuild.so to exist
# under %LocalAppData%\programs\python\python38\lib\site-packages
# or $HOME/.local/lib/python3.8/site-packages 
import nbuild

# Start with a project description;
# where are the artifacts?
# how do we build the artifacts?
# what is the expected output?
p = nbuild.Project(
  name='Wunderwaffe Artillery',
  
  deliverables_in=nbuild.physical_items(
    "One Schwerer Gustav 80-cm railway gun",
    "One 7-ton 80cm Shell"
  ),

  build_system=nbuild.physical_prep(
    "Ensure railway gun is bolted to track such that it cannot move when force is applied",
    "Rest 500lb of sandbags behind gun to prevent knockback from moving gun",
    "Place disposable target 30 miles away and establish 5 mile fire zone around target"
  ),

  test_system=nbuild.physical_test(
    # Lines beginning with "I:" are instructions, operators press enter to continue.
    # Lines beginning with "Q:" are questions, operators prett "y" or "n" in response.
    "I: Ensure fire zone is clear",
    "I: Aim railway gun at target",
    "I: Load 7-ton shell into railway gun",
    "I: Fire railway gun",
    "Q: Was the target hit?",
    "Q: Was the target destroyed?"
  )

)

p.build()

p.test()

p.write_reports_to('reports')
# This calls the default OS handler for reports (usually a web browser)
p.open_reports()


