from typing import List, Dict
from photomanager.lib.pmconst import PATH_SEP
from photomanager.lib import errors
from photomanager.controller.controller_base import UIControllerBase
from photomanager.lib.errors import RemoveImageIndexOutofRangeError, RemoveImageCannotRemoveAllError
from photomanager.utils.action_executor import ActionRemoveFile
from PyQt5.QtGui import QImage
from PyQt5 import QtCore

class DispImageController(UIControllerBase):

    def __init__(self, base_folder: str, db_session, ui_data):
        super().__init__(base_folder, db_session, ui_data)
        if not ui_data:
            raise ValueError

        self.image_infos: List[Dict] = ui_data
        self.index = 0

    @property
    def image_count(self):
        return len(self.image_infos)

    def next(self):
        self.index = self.index + 1
        if self.index == self.image_count:
            self.index = 0

    def prev(self):
        self.index = self.index - 1
        if self.index < 0:
            self.index = self.image_count - 1

    @property
    def current_image_info(self):
        return self.image_infos[self.index]

    def get_current_image(self, size: QtCore.QSize) -> QImage:
        full_name = self.base_folder + PATH_SEP + self.current_image_info['folder'] + \
                    PATH_SEP + self.current_image_info['filename']
        disp_img = QImage(full_name)
        disp_img.load(full_name)

        scaled_img = disp_img.scaled(size,  QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return scaled_img
