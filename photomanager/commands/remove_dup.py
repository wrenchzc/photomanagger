# -*- coding: utf-8 -*-
import os
from photomanager.commands.base import Command
from sqlalchemy import func, desc
from photomanager.db.models import ImageMeta


class CommandRemoveDuplicate(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)

    def do(self):
        if self.params.get("duplicate"):
            self._list_duplicate()

    def _list_duplicate(self):
        dup_md5s = self.handler.session.query(func.count(ImageMeta.md5), ImageMeta.md5).group_by(ImageMeta.md5).having(
            func.count(ImageMeta.md5) > 1).order_by(desc(func.count(ImageMeta.md5))).all()

        dup_md5 = {}
        dup_folder = {}
        dup_file = {}

        for result_md5 in dup_md5s:
            md5 = result_md5.md5
            dup_files = self.handler.session.query(ImageMeta.filename).filter(ImageMeta.md5 == md5).all()
            # print("{cnt} items have same md5 {md5}".format(cnt=len(dup_files), md5=md5))
            for dup_file in dup_files:
                filename = os.path.basename(dup_file)


                 # print(dup_file.filename)

