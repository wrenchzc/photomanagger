import os
from src.pmconst import PM_TODO_LIST, PM_TODO_INDEX
from src.commands.base import Command
from src.imageutils import get_folder_image_files


class CommandIndex(Command):
    def __init__(self, folder, params):
        super().__init__(folder, params)
        self.todo_inx = 0

    def do(self):
        self.get_file_list()
        self.index()

    def _todo_file_existed(self):
        self.todo_file = "{folder}{sep}{list_file}".format(folder=self.folder, sep=os.path.sep, list_file=PM_TODO_LIST)
        self.index_file = "{folder}{sep}{index_file}".format(folder=self.folder, sep=os.path.sep,
                                                             index_file=PM_TODO_INDEX)

        return os.path.exists(self.todo_file) and os.path.exists(self.index_file)

    def _resume_file_list(self):
        with open(self.todo_file) as fp_todb:
            self.file_list = fp_todb.read()

        with open(self.todo_file) as fp_inx:
            self.todo_inx = int(fp_inx.read())

    def _get_file_list_from_folder(self):
        self.file_list = get_folder_image_files(self.folder)

    def get_file_list(self):
        if self._todo_file_existed():
            self._resume_file_list()
        else:
            self._get_file_list_from_folder()

    def index(self):
        pass
