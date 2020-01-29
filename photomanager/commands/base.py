import os
from photomanager.db.dbutils import get_db_session
from photomanager.pmconst import PMDBNAME, PATH_SEP

class Command(object):
    def __init__(self, folder, params):
        self.folder = os.path.expanduser(folder.rstrip("/\\"))
        self.params = params
        self.db_session = get_db_session(self.folder + PATH_SEP + PMDBNAME)

    def do(self):
        raise NotImplemented

    def __del__(self):
        self.db_session.close()
