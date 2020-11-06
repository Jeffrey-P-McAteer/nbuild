
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
  name='NASA WorldWind',
  
  # The git_dir argument is optional - if omitted a new temporary directory will be used
  deliverables_in=nbuild.git_repository(
    "https://github.com/WorldWindEarth/worldwindjs", git_dir="/tmp/worldwindjs"
  ),
  
  build_system=nbuild.npm_build('run', 'build'),
  test_system=nbuild.npm_test('run', 'test')

)

p.build()

p.test()

p.write_reports_to('reports')
# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




