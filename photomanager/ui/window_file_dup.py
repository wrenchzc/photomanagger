from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from photomanager.ui.ui_file_dup import Ui_DlgFileDup
from photomanager.pmconst import PATH_SEP


class WindowClearDup(QDialog, Ui_DlgFileDup):
    def __init__(self, folder: str, dup_files_by_md5: dict, parent=None):
        super(WindowClearDup, self).__init__(parent)
        self.folder = folder
        self.dup_files_by_md5 = dup_files_by_md5
        self.__init__ui__()
        self.__init__data__()
        self.__init_by_dup_files__()

    def __init__data__(self):
        self.dup_keys = list(self.dup_files_by_md5)
        self.active_key = None
        self.active_files = []
        self.active_index = 0

    def __init__ui__(self):
        self.setupUi(self)
        self.setModal(True)
        self.lblImage.setScaledContents(True)
        self.btnDelete.setEnabled(False)

    def __init_by_dup_files__(self, selected_index = 0):
        self.lstDupFiles.clear()
        self.active_key = self.dup_keys[self.active_index]
        self.active_files = self.dup_files_by_md5[self.active_key]

        for item in self.active_files:
            self.lstDupFiles.addItem(item[0] + PATH_SEP + item[1])
        first_folder, first_name = self.active_files[selected_index]
        first_full_name = self.folder + PATH_SEP + first_folder + PATH_SEP + first_name
        disp_img = QImage(first_full_name)
        disp_img.load(first_full_name)
        self.lblImage.setPixmap(QPixmap.fromImage(disp_img))

        if self.lstDupFiles.count() > 0:
            pass

    def btnNext_click(self):
        if self.active_index < len(self.dup_keys) - 1:
            self.active_index = self.active_index + 1
            self.__init_by_dup_files__()

    def btnPrev_click(self):
        if self.active_index > 0:
            self.active_index = self.active_index - 1
            self.__init_by_dup_files__()
    
    def lstDupFiles_itemSelectChanged(self):
        self.btnDelete.setEnabled(len(self.lstDupFiles.selectedItems()) > 0)

    def lstDupFile_itemActivated(self, list_item: QListWidgetItem):
        select_index = self.lstDupFiles.currentRow()
        self.__init_by_dup_files__(select_index)