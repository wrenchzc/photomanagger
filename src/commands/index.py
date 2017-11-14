import os
from src.pmconst import PM_TODO_LIST, PM_TODO_INDEX, PMDBNAME
from src.commands.base import Command
from src.imageutils import get_folder_image_files
from src.db.imagehandler import ImageDBHandler
from src.db.dbutils import get_db_session

line_sep = "\r\n"


class CommandIndex(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)
        self.todo_inx = 0
        self.force = params.get("force", False)
        self.todo_file_name = "{folder}{sep}{list_file}".format(folder=self.folder, sep=os.path.sep,
                                                                list_file=PM_TODO_LIST)
        self.index_file_name = "{folder}{sep}{index_file}".format(folder=self.folder, sep=os.path.sep,
                                                                  index_file=PM_TODO_INDEX)
        self.fp_index = None

    def do(self):
        self.get_file_list()
        self.index()

    def _todo_file_existed(self):
        return os.path.exists(self.todo_file_name) and os.path.exists(self.index_file_name)

    def _resume_file_list(self):
        with open(self.todo_file_name) as fp_todb:
            self.file_list = fp_todb.read().split(line_sep)

        self.fp_index = open(self.index_file_name, "a+")
        self.fp_index.seek(0)
        self.todo_inx = int(self.fp_index.read())

    def _set_todo_index(self, index_num):
        if not self.fp_index:
            raise ValueError("{index} should be writeable".format(index=self.index_file_name))

        self.fp_index.seek(0)
        self.fp_index.truncate()
        self.fp_index.write(str(index_num))
        self.fp_index.flush()

    def _get_file_list_from_folder(self):
        self.file_list = get_folder_image_files(self.folder)
        with open(self.todo_file_name, "w") as fp_todo:
            fp_todo.write(line_sep.join(self.file_list))

        self.fp_index = open(self.index_file_name, "w")
        self._set_todo_index(0)

    def get_file_list(self):
        if not self._todo_file_existed() or self.force:
            self._get_file_list_from_folder()
        else:
            self._resume_file_list()

    def index(self):
        db_session = get_db_session(self.folder + os.path.sep + PMDBNAME)
        self.handler = ImageDBHandler(self.folder, db_session)
        self.handler.do_index(self.file_list[self.todo_inx:])
        db_session.close()
