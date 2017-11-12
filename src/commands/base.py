import os


class Command(object):
    def __init__(self, folder, params):
        self.folder = folder.rstrip(os.path.sep)
        self.params = params

    def do(self):
        raise NotImplemented
