import os
from src.db.imagehandler import ImageDBHandler
from src.pmconst import PMDBNAME


class ImageIndexer:
    def __init__(self, folder, force):
        folder = os.path.expanduser(folder)
        if not os.path.exists(folder):
            raise IOError("folder {folder} does not existed".format(folder))
        self._folder = folder
        self._forceupdate = force
        self._handler = ImageDBHandler()

    @property
    def need_resume(self):
        pass

    def get_resumt_id(self):
        pass

    def do_init_image_db(self):
        pass

    def do_index(self, start_id):
        pass

    def do(self):
        if self.need_resume:
            start_id = self.get_resumu_id()
        else:
            start_id = self.do_init_image_db()

        self.do_index(start_id)
