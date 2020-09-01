# -*- coding: utf-8 -*-
import os
from photomanager.commands.base import Command
from sqlalchemy import func, desc
from photomanager.db.models import ImageMeta
from photomanager.utils.logger import logger
from photomanager.ui.qt_app import qt_app
from photomanager.ui.window_file_dup import WindowClearDup


class CommandRemoveDuplicate(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)

    def do(self):
        dups = self._list_duplicate()
        self._do_clean(dups)
        #for md5 in dups.keys():
        #    self._do_clean(dups[md5])

    def _do_clean(self, dup_files_by_md5):
        w_file_dup = WindowClearDup(self.folder, dup_files_by_md5)
        w_file_dup.show()
        qt_app.exec_()


    def _list_duplicate(self) -> dict:
        dup_md5s = self.db_session.query(func.count(ImageMeta.md5), ImageMeta.md5).group_by(ImageMeta.md5).having(
            func.count(ImageMeta.md5) > 1).order_by(desc(func.count(ImageMeta.md5))).all()

        dup_grpup_by_md5 = {}

        for result_md5 in dup_md5s:
            md5 = result_md5.md5
            dup_files = self.db_session.query(ImageMeta.folder, ImageMeta.filename).filter(ImageMeta.md5 == md5).all()
            dup_grpup_by_md5[md5] = [(dup_file.folder, dup_file.filename) for dup_file in dup_files]

        return dup_grpup_by_md5

