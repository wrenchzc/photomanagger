from typing import List
from photomanager.pmconst import PATH_SEP
from photomanager import errors
from photomanager.controller.controller_base import UIControllerBase
from photomanager.db.models import ImageMeta
from photomanager.errors import RemoveImageIndexOutofRangeError, RemoveImageCannotRemoveAllError
from photomanager.utils.action_executor import ActionRemoveFile
from PyQt5.QtGui import QImage 

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

class FileDupController(UIControllerBase):

    def __before_show__(self):
        self.dup_files_by_md5 = self.ui_data
        self.dup_keys = list(self.dup_files_by_md5)
        self.__init_data__()
        self.active_index = 0

    def __init_data__(self):
        self._active_index = None
        self.active_files = []
        self.current_dup_files = []

    @property
    def active_index(self) -> int:
        return self._active_index

    @active_index.setter
    def active_index(self, active_index = 0):
        if not self.dup_files_by_md5:
            self.__init_data__()

        self._active_index = active_index
        self.active_key = self.dup_keys[self.active_index]
        self.active_files = self.dup_files_by_md5[self.active_key]
        self.current_dup_files = []
        for item in self.active_files:
            rel_path, base_name = item
            rel_name = base_name if rel_path == "" else f"{rel_path}{PATH_SEP}{base_name}"
            self.current_dup_files.append(rel_name)

    def next(self):
        if self.active_index < len(self.dup_keys) - 1:
            self.active_index = self.active_index + 1

    def prev(self):
        if self.active_index > 0:
            self.active_index = self.active_index - 1

    @property
    def current_dupfiles_count(self) -> int:
        return len(self.current_dup_files)

    @property
    def dup_group_count(self) -> int:
        return len(self.dup_keys)

    def delete_current_dups_by_indexs(self, indexs: List[int]):
        if not self.dup_files_by_md5:
             raise errors.RemoveImageIndexOutofRangeError()

        old_active_index = self.active_index
        old_current_list_count = self.current_dupfiles_count
        old_dup_list_count = self.dup_group_count

        remove_dup_doer = RemoveDupFilesDoer(self.base_folder, self.db_session, self.active_files)
        del_cnt = remove_dup_doer.delete(indexs)

        if del_cnt == old_current_list_count - 1:
            self.dup_files_by_md5.pop(self.active_key)
            self.dup_keys = list(self.dup_files_by_md5)

            if old_active_index == old_dup_list_count - 1:
                self.active_index = len(self.dup_keys) - 1
            else:
                self.active_index = old_active_index
        else:
            self.active_index = old_active_index

    def index_image(self, index: int):
        first_full_name = self.base_folder + PATH_SEP + self.current_dup_files[index]
        disp_img = QImage(first_full_name)
        disp_img.load(first_full_name)
        return disp_img

    