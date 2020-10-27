import typing
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from photomanager.ui.ui_disp_image import Ui_dlgDispImage
from photomanager.controller.controller_disp_image import DispImageController


class WindowDispImage(QDialog, Ui_dlgDispImage):

    def __init__(self, folder: str, db_session, image_info_list: typing.List[typing.List], parent=None):
        super(WindowDispImage, self).__init__(parent)
        self.base_folder = folder
        self.session = db_session
        self.image_infos = image_info_list
        self.controller = DispImageController(folder, db_session, self.image_infos)

        self.__init__ui__()
        self.__refresh_ui__()

    def __init__ui__(self):
        self.setupUi(self)
        self.setModal(True)
        self.lblImage.setScaledContents(True)

    def __refresh_ui__(self):
        disp_img = self.controller.current_image
        self.lblImage.setPixmap(QPixmap.fromImage(disp_img))
        self.lblIndex.setText(f"{self.controller.index + 1}/{self.controller.image_count}")
        self.lstInfo.clear()
        for field in self.controller.current_image_info:
            val = self.controller.current_image_info[field]
            field_info = f"{field}:  {val}"
            item = self.lstInfo.addItem(field_info)

    def next_clicked(self):
        self.controller.next()
        self.__refresh_ui__()


    def prev_clicked(self):
        self.controller.prev()
        self.__refresh_ui__()