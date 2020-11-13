
"""
The deliverable module holds the Deliverable class
"""

class Deliverable:
    """
    The Deliverable class holds references to delivered assets.
    These may be queried later by tests and tasks such as build systems
    which need to know CWD data and execution tasks which need deliverable
    file names to execute.
    """
    def __init__(self, type_, **kwargs):
        if not type_:
            raise Exception("Error: Deliverable requires type_")
        self.type_ = type_
        self.kwargs = dict(kwargs)

    def get_cwd(self):
        """
        currently only implemented for deliverable of type 'SW_Repository'.
        Returns a working directory for this deliverable, or raises an
        exception if it does not make sense for this deliverable to have a CWD.
        """
        if self.type_ == 'SW_Repository':
            if self.kwargs['directory']:
                return self.kwargs['directory']
            else:
                raise Exception('TODO, clone git/svn repo to temp dir (also maybe .zip /.tar archives as well over https)')
        else:
            raise Exception('Cannot get_cwd for Deliverable of type_={}'.format(self.type_))

