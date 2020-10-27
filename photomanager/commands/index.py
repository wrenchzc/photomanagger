import os
from photomanager.lib.pmconst import PM_TODO_LIST, PATH_SEP
from photomanager.commands.base import Command
from photomanager.utils.imageutils import get_folder_image_files
from photomanager.lib.helper import current_time_str
from photomanager.db.imagehandler import ImageDBHandler
from photomanager.db.models import ImageMeta


class CommandIndex(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)
        self.todo_inx = 0
        self.force = params.get("force", False)
        self.skip_existed = params.get("skip_existed", False)
        self.clean = params.get("clean", False)
        self.handler = ImageDBHandler(folder, self.db_session, skip_existed=self.skip_existed)

        self.todo_file_name = os.path.expanduser("{folder}{sep}{list_file}".format(folder=self.folder, sep=PATH_SEP,
                                                                                   list_file=PM_TODO_LIST))
        self.fp_index = None
        self.handler.on_index_image = self.on_index_image
        self.restart_inx = 0

    def do(self):
        self.get_file_list()
        index_count = self.index()
        del_count = self.do_clean() if self.clean else 0
        return index_count, del_count

    def do_clean(self):
        all_file_list = get_folder_image_files(self.folder, 0)

        images_meta = self.db_session.query(ImageMeta).all()
        total_count = len(images_meta)
        del_count = 0
        count = 0
        for image_meta in images_meta:
            count += 1
            if count % 1000 == 0:
                print(f"{count}/{total_count}")

            if image_meta.get_filename_with_folder() not in all_file_list:
                self.db_session.delete(image_meta)
                del_count += 1
                print("delete recode for {}".format(image_meta.filename))
        self.db_session.commit()
        return del_count

    def _resume_file_list(self):
        with open(self.todo_file_name, encoding='utf-8') as fp_todb:
            self.file_list = fp_todb.readlines()

        self.todo_inx = self.handler.todo_index
        self.restart_inx = self.todo_inx

    def _set_todo_index(self, index_num):
        self.handler.todo_index = index_num

    def _get_file_list_from_folder(self):
        if self.force:
            last_index_time_str = 0
        else:
            last_index_time_str = self.config.get_value("INDEX_END_TIME")

        self.file_list = get_folder_image_files(self.folder, last_index_time_str)
        with open(self.todo_file_name, "w", encoding='utf-8') as fp_todo:
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
        self.config.set_value("INDEX_BEGIN_TIME", current_time_str())
        self.config.set_value("INDEX_END_TIME", None)
        cnt = self.handler.do_index(self.file_list[self.todo_inx:])
        self.config.set_value("INDEX_END_TIME", current_time_str())
        os.remove(self.todo_file_name)
        self.handler.todo_index = -1
        return cnt

    def on_index_image(self, inx):
        real_inx = inx + self.restart_inx
        if real_inx % 100 == 0:
            self._set_todo_index(real_inx)
        print("{filename}   {inx}/{total}".format(filename=self.file_list[inx + self.restart_inx],
                                                  inx=inx + self.restart_inx, total=len(self.file_list)))
