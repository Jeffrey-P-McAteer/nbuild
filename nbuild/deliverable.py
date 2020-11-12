
class Deliverable:
    def __init__(self, type_, **kwargs):
        if not type_:
            raise Exception("Error: Deliverable requires type_")
        self.type_ = type_
        self.kwargs = dict(kwargs)

    def get_cwd(self):
        if self.type_ == 'SW_Repository':
            if self.kwargs['directory']:
                return self.kwargs['directory']
            else:
                raise Exception('TODO, clone git/svn repo to temp dir (also maybe .zip /.tar archives as well over https)')
        else:
            raise Exception('Cannot get_cwd for Deliverable of type_={}'.format(self.type_))

