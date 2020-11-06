
import os
import sys
import subprocess

if __name__ == '__main__':
  
  subprocess.run([
    'pylint', 'nbuild'
  ], check=False)

  # Running
  #    python do_quality_checks.py edit subl3
  # will cause us to re-execute pylint and parse the
  # results, passing files to the command "subl3" for editing.
  if len(sys.argv) > 2 and sys.argv[1] == 'edit-with':
    print("")
    print("Opening first task in IDE...")
    print("")
    proc = subprocess.Popen(['pylint', 'nbuild'], stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
      if not isinstance(line, str):
        line = line.decode('utf-8')

      if 'nbuild' in line and '.py' in line:
        # We have something to fix!
        print(line.strip())
        print("")
        file_and_line = line.split(': ')[0]
        subprocess.run([sys.argv[2], file_and_line])
        break



