class Command(object):
    def __init__(self, folder, params):
        self.folder = folder.rstrip("/\\")
        self.params = params

    def do(self):
        raise NotImplemented
