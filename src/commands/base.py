class Command(object):

    def __init__(self, folder, params):
        self.folder = folder
        self.params = params


    def do(self):
        raise NotImplemented

