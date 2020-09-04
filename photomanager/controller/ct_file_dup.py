from typing import List
from photomanager import 
from photomanager.controller.controller_base import UIControllerBase


class FileDupController(UIControllerBase):

    def __before_show__(self):
        self.dup_files_by_md5 = self.ui_data
        self.dup_keys = list(self.dup_files_by_md5)
        self.active_key = None
        self.active_files = []
        self.active_index = 0

    def set_active(self, active_index = 0):
        self.active_index = active_index
        self.active_key = self.dup_keys[self.active_index]
        self.active_files = self.dup_files_by_md5[self.active_key]
        self.current_dup_files = []
        for item in self.active_files:
            self.current_dup_files.append(item[0] + PATH_SEP + item[1])


    def next(self):
        if self.active_index < len(self.dup_keys) - 1:
            self.active_index = self.active_index + 1

    def prev(self):
        if self.active_index > 0:
            self.active_index = self.active_index - 1

    @property
    def current_dupfiles_count(self):
        return len(self.dup.keys)
