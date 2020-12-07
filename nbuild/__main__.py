
import subprocess
import sys
import os

def help():
  print("""Usage: python -m nbuild /path/to/project.py

""")

if __name__ == '__main__':
  if len(sys.argv) < 2:
    help()
    sys.exit(1)

  project_file = os.path.abspath(sys.argv[1])
  project_dir = os.path.dirname(project_file)

  print("Evaluating {} in {}".format(project_file, project_dir))

  os.chdir(project_dir)

  subprocess.run([
    sys.executable, project_file
  ])

