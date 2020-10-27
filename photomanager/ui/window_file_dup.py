from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from photomanager.ui.ui_file_dup import Ui_DlgFileDup
from photomanager.controller.controller_file_dup import FileDupController
from photomanager.lib import errors


class WindowClearDup(QDialog, Ui_DlgFileDup):
    def __init__(self, folder: str, db_session, dup_files_by_md5: dict, parent=None):
        super(WindowClearDup, self).__init__(parent)
        self.controller = FileDupController(folder, db_session, dup_files_by_md5)
        self.folder = folder
        self.__init__ui__()
        self.__refresh_ui__(True)

    def __init__ui__(self):
        self.setupUi(self)
        self.setModal(True)
        self.lblImage.setScaledContents(True)
        self.btnDelete.setEnabled(False)

    def __refresh_ui__(self, refresh_list = False, selected_index = 0):
        if refresh_list:
            self.lstDupFiles.clear()
            for item_text in self.controller.current_dup_files:
                self.lstDupFiles.addItem(item_text)

        disp_img = self.controller.index_image(selected_index)
        self.lblImage.setPixmap(QPixmap.fromImage(disp_img))

        self.btnPrev.setEnabled(self.controller.active_index != 0)
        self.btnNext.setEnabled(self.controller.active_index != self.controller.dup_group_count - 1)


    def btnNext_click(self):
        self.controller.next()
        self.__refresh_ui__(True)


    def btnPrev_click(self):
        self.controller.prev()
        self.__refresh_ui__(True)

    def btnDelete_click(self):
        selected_indexs = [self.lstDupFiles.row(item) for item in self.lstDupFiles.selectedItems()]

        rel_filenames = [self.controller.current_dup_files[inx] for inx in selected_indexs]
        query_msg = f"{rel_filenames} will be deleted, please confirm"
        r = QMessageBox.question(self, "confirm", query_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if r == QMessageBox.Yes:
            try:
                self.controller.delete_current_dups_by_indexs(selected_indexs)
            except errors.RemoveImageCannotRemoveAllError:
                QMessageBox.critical(self, "error", "can not delete all images for a group", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "error", str(e), QMessageBox.Ok)
            
            self.__refresh_ui__(True)

    
    def lstDupFiles_itemSelectChanged(self):
        selected_count = len(self.lstDupFiles.selectedItems())
        self.btnDelete.setEnabled(selected_count > 0)
        if selected_count > 0:
            current_index = self.lstDupFiles.currentRow()
            if current_index >= 0:
                self.__refresh_ui__(False, current_index)

