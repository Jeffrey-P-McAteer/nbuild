
import os

# Import nbuild; this requires nbuild.so to exist
# under %LocalAppData%\programs\python\python38\lib\site-packages
# or $HOME/.local/lib/python3.8/site-packages 
import nbuild

this_dir = os.path.dirname(os.path.abspath(__file__))

# Start with a project description;
# where are the artifacts?
# how do we build the artifacts?
# what is the expected output?
p = nbuild.Project(
  name='Project 01',
  
  # What is handed to the reviewer by the contractor - webpage URL, directory of .exe files, shapefile containing a map, etc.
  deliverables_in=nbuild.src_directory(
    os.path.join(this_dir, 'proj01')
  ),
  
  # Optional - defaults to nbuild.nobuild(), which does nothing.
  # In this case deliverables_out == deliverables_in
  build_system=nbuild.make(),

  # Optional: If any specified deliverables do not exist after
  # running the build then the build step fails.
  deliverables_out=nbuild.executable(
    os.path.join(this_dir, 'proj01', 'main.exe')
  ),

  # The test system describes operations done on the deliverables
  # and has functions for specifying correctness.
  test_system=nbuild.execute(
    os.path.join(this_dir, 'proj01', 'main.exe'), 'John Smith'
  )
  .with_stdout(
    'The program main.exe uses "hello" to greet the user.',
    lambda stdout: 'hello' in stdout.lower()
  )
  .with_stdout(
    'The program main.exe, when called with arg1 of "John Smith" greets John Smith.',
    lambda stdout: 'Hello John Smith' in stdout
  )

)

# Now that the project is described we can
# generate flowcharts using graphviz
p.write_flowcharts_to(os.path.join(this_dir, 'reports'))

p.build()

p.test()

p.write_reports_to(os.path.join(this_dir, 'reports'))
# This calls the default OS handler for reports (usually a web browser)
p.open_reports()




