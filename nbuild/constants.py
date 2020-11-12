
from nbuild.deliverable import Deliverable

# These constants are merely used as words/types in other systems
# Avoid using falsey values like "", 0, or [] because we often use None
# values as defaults and test if variables have been set with "if not X: raise Exception('must specify X')"
SW_Application = 1

def SW_Repository(url=None, directory=None):
  if not url and not directory:
    raise Exception("SW_Repository created without url or directory, one must be specified.")

  return Deliverable(
    type_='SW_Repository',
    url=url,
    directory=directory,
  )



