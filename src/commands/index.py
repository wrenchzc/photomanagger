import os
from src.pmconst import PM_TODO_LIST, PMDBNAME
from src.commands.base import Command
from src.imageutils import get_folder_image_files
from src.db.imagehandler import ImageDBHandler
from src.db.dbutils import get_db_session
from src.helper import current_time_str


class CommandIndex(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)
        self.todo_inx = 0
        self.force = params.get("force", False)
        self.todo_file_name = os.path.expanduser("{folder}{sep}{list_file}".format(folder=self.folder, sep=os.path.sep,
                                                                                   list_file=PM_TODO_LIST))
        self.fp_index = None
        self.db_session = get_db_session(self.folder + os.path.sep + PMDBNAME)
        self.handler = ImageDBHandler(self.folder, self.db_session)
        self.handler.on_index_image = self.on_index_image

    def do(self):
        self.get_file_list()
        self.index()

    def _todo_file_existed(self):
        return os.path.exists(self.todo_file_name)

    def _resume_file_list(self):
        with open(self.todo_file_name) as fp_todb:
            self.file_list = fp_todb.readlines()

        self.todo_inx = self.handler.todo_index

    def _set_todo_index(self, index_num):
        self.handler.todo_index = index_num

    def _get_file_list_from_folder(self):
        self.file_list = get_folder_image_files(self.folder)
        with open(self.todo_file_name, "w") as fp_todo:
            fp_todo.write("\n".join(self.file_list))

        self._set_todo_index(0)

    def get_file_list(self):
        if not os.path.exists(self.todo_file_name) and self.handler.todo_index != -1:
            self.handler.todo_index = -1

        if self.handler.todo_index == -1 or self.force:
            self._get_file_list_from_folder()
        else:
            self._resume_file_list()

    def index(self):
        self.handler.set_option_value("INDEX_BEGIN_TIME", current_time_str())
        self.handler.set_option_value("INDEX_END_TIME", None)
        self.handler.do_index(self.file_list[self.todo_inx:])
        self.handler.set_option_value("INDEX_END_TIME", current_time_str())

    def on_index_image(self, inx):
        self._set_todo_index(inx)
        print("{filename}   {inx}/{total}".format(filename=self.file_list[inx], inx=inx, total=len(self.file_list)))
