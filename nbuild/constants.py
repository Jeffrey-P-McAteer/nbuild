
"""
The constants module holds identifiers and
small functions which create deliverables/tests/tasks.
This module mostly handles converting human-readable language
(such as "Software Application") into the types used within nbuild
(such as Deliverable(type_='SW_Repository')) so that project
authors do not need to know a huge amount about nbuild's internal structure to make use of it.
"""


from nbuild.deliverable import Deliverable

# These constants are merely used as words/types in other systems
# Avoid using falsey values like "", 0, or [] because we often use None
# values as defaults and test if variables have been set with "if not X: raise Exception('must specify X')"
SW_Application = 1

def SW_Repository(url=None, directory=None):
    """Creates a Deliverable of type SW_Repository"""
    if not url and not directory:
        raise Exception("SW_Repository created without url or directory, one must be specified.")

    return Deliverable(
        type_='SW_Repository',
        url=url,
        directory=directory,
    )



