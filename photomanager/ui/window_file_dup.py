from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from photomanager.ui.ui_file_dup import Ui_DlgFileDup
from photomanager.pmconst import PATH_SEP
from photomanager.controller.controller_file_dup import FileDupController

class WindowClearDup(QDialog, Ui_DlgFileDup):
    def __init__(self, folder: str, db_session, dup_files_by_md5: dict, parent=None):
        super(WindowClearDup, self).__init__(parent)
        self.controller = FileDupController(folder, db_session, dup_files_by_md5)
        self.folder = folder
        self.__init__ui__()
        self.__refresh_ui__()

    def __init__ui__(self):
        self.setupUi(self)
        self.setModal(True)
        self.lblImage.setScaledContents(True)
        self.btnDelete.setEnabled(False)

    def __refresh_ui__(self, selected_index = 0):
        self.lstDupFiles.clear()
        for item_text in self.controller.current_dup_files:
            self.lstDupFiles.addItem(item_text)

        disp_img = self.controller.index_image(selected_index)
        self.lblImage.setPixmap(QPixmap.fromImage(disp_img))

    def btnNext_click(self):
        self.controller.next()
        self.__refresh_ui__()


    def btnPrev_click(self):
        self.controller.prev()
        self.__refresh_ui__()
    
    def lstDupFiles_itemSelectChanged(self):
        selected_count = len(self.lstDupFiles.selectedItems())
        self.btnDelete.setEnabled(selected_count > 0)
        if selected_count > 0:
            current_index = self.lstDupFiles.currentRow()
            if current_index >= 0:
                self.__refresh_ui__(current_index)

