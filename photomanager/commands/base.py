import os

class Command(object):
    def __init__(self, folder, params):
        self.folder = os.path.expanduser(folder.rstrip("/\\"))
        self.params = params

    def do(self):
        raise NotImplemented
