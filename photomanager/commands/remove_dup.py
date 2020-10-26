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
            dups = self._list_duplicate()
            for md5 in dups.keys():
                self._do_clean(dups[md5])

    def _do_clean(self, dup_files_by_folder):
        pass

    def _list_duplicate(self) -> dict:
        dup_md5s = self.handler.session.query(func.count(ImageMeta.md5), ImageMeta.md5).group_by(ImageMeta.md5).having(
            func.count(ImageMeta.md5) > 1).order_by(desc(func.count(ImageMeta.md5))).all()

        dup_grpup_by_md5 = {}

        for result_md5 in dup_md5s:
            md5 = result_md5.md5
            dup_files = self.handler.session.query(ImageMeta.filename).filter(ImageMeta.md5 == md5).all()
            dup_grpup_by_md5[md5] = self._get_dup_files_group_by_folder(dup_files)

        return dup_grpup_by_md5

    def _get_dup_files_group_by_folder(self, dup_files: list) -> dict:
        """
        :param dup_files: list of files
        :return: dict
        sample:
            {"folder1", "aaa.jpg", "bbb.jpg",
             "folder2", "aaa.jpg"
            }

        """
        dup_files_by_folder = {}
        for dup_file in dup_files:
            file_name = os.path.basename(dup_file)
            foldler_name = os.path.dirname(dup_file)
            if foldler_name not in dup_files_by_folder:
                dup_files_by_folder[foldler_name] = []
            dup_files_by_folder[foldler_name].append(file_name)
        return dup_files_by_folder
