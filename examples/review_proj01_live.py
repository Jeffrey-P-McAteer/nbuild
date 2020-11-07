
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
  
  build_system=nbuild.make(),

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

# This will run a server on http://localhost:8080
# where the deliverable source or .exe files may
# be uploaded and a report generated.
# There is no limit to how many times the tests may be run.
p.run_test_server()


