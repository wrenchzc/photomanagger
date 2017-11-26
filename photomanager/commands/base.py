import os
from photomanager.db.imagehandler import ImageDBHandler
from photomanager.db.dbutils import get_db_session
from photomanager.pmconst import PMDBNAME

class Command(object):
    def __init__(self, folder, params):
        self.folder = os.path.expanduser(folder.rstrip("/\\"))
        self.params = params
        self.db_session = get_db_session(self.folder + os.path.sep + PMDBNAME)
        self.handler = ImageDBHandler(self.folder, self.db_session)

    def do(self):
        raise NotImplemented
