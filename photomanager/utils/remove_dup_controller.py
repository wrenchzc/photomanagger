from typing import List
from sqlalchemy import func, desc, and_
from photomanager.pmconst import PATH_SEP
from photomanager.db.models import ImageMeta
from photomanager.errors import RemoveImageIndexOutofRangeError, RemoveImageCannotRemoveAllError
from photomanager.utils.action_executor import ActionRemoveFile


class RemoveDupFilesDoer(object):

    def __init__(self, base_folder: str, db_session, dup_files: list):
        """
        dup_files: list, example  [('', 'test4.jpg'), ('', 'test4_dup.jpg'), ('subdir', 'test4_dup.jpg')]

        """
        self.base_folder = base_folder
        self.db_session = db_session
        self.dup_files = dup_files

    def delete(self, del_indexs: List[int]):
        for del_index in set(del_indexs):
            if not self._check_del_index(del_index):
                raise RemoveImageIndexOutofRangeError()

        if len(del_indexs) == len(self.dup_files):
            raise RemoveImageCannotRemoveAllError()

        cnt = len(self.dup_files)
        del_cnt = 0
        for i in range(cnt - 1, -1, -1):
            if i in del_indexs:
                self.__do_remove_file(i)
                self.dup_files.pop(i)
                del_cnt = del_cnt + 1
        return del_cnt

    def __do_remove_file(self, del_index):
        del_item = self.dup_files[del_index]
        folder, fname = del_item
        if folder == "":
            rel_name = fname
        else:
            rel_name = f"{folder}{PATH_SEP}{fname}"
        remove_action = dict(action="remove_file", files=[rel_name])
        remove_executor = ActionRemoveFile(self.base_folder, self.db_session, remove_action)
        remove_executor.do()
    def _check_del_index(self, del_index):
        if del_index < 0 or del_index > len(self.dup_files) - 1:
            return False
        return True
