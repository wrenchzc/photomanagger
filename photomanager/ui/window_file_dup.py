from PyQt5.QtWidgets import QDialog
from photomanager.ui.ui_file_dup import Ui_DlgFileDup
from photomanager.pmconst import PATH_SEP


class WindowClearDup(QDialog, Ui_DlgFileDup):
    def __init__(self, dup_files_by_md5: dict, parent=None):
        super(WindowClearDup, self).__init__(parent)
        self.dup_files_by_md5 = dup_files_by_md5
        self.dup_keys = list(dup_files_by_md5)
        self.active_key = None
        self.active_files = []
        if len(self.dup_keys) > 0:
            self.active_key = self.dup_keys[0]
            self.active_files = self.dup_files_by_md5[self.active_key]
        self.setupUi(self)
        self.setModal(True)

        self.__init_by_dup_files__()

    def __init_by_dup_files__(self):
        for item in self.active_files:
            self.lstDupFiles.addItem(item[0] + PATH_SEP + item[1])

        if self.lstDupFiles.count() > 0:
            pass
