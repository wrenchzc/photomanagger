import os
import typing
from photomanager.db.dbutils import get_db_session, close_db_session
from photomanager.pmconst import PMDBNAME, PATH_SEP
from photomanager.db.config import Config


class Command(object):
    def __init__(self, folder: str, params: typing.Dict):
        self.folder = os.path.expanduser(folder.rstrip("/\\"))
        self.params = params
        self.db_session = get_db_session(self.folder + PATH_SEP + PMDBNAME)
        self.config = Config(self.db_session)

    def do(self):
        raise NotImplementedError

    def __del__(self):
        close_db_session(self.db_session)
