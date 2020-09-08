import os
import platform
from photomanager.db.models import ImageMeta
from sqlalchemy import and_
from photomanager.errors import MultiFileError
from photomanager.pmconst import PATH_SEP


class ActionExecutor(object):

    def __init__(self, base_folder: str, db_session, action_item: dict):
        self.base_folder = base_folder
        self.db_session = db_session
        self.action_item = action_item

    def do(self):
        raise NotImplementedError


class ActionRemoveFile(ActionExecutor):

    def do(self):
        if self.action_item["action"] != "remove_file":
            raise ValueError

        for relative_file in self.action_item["files"]:
            self.do_remove_file(relative_file)

    def do_remove_file(self, relative_filename):
        self._do_remove_file_from_disk(relative_filename)
        self._do_remove_file_from_db(relative_filename)

    def _do_remove_file_from_disk(self, relative_filename):
        full_base_folder = self.base_folder
        if platform.system() == "Linux" and not self.base_folder.startswith(PATH_SEP):  # relative path:
            full_base_folder = os.getcwd() + PATH_SEP + self.base_folder
        elif platform.system() == "Windows" and not self.base_folder[1] == ":":
            full_base_folder = os.getcwd() + PATH_SEP + self.base_folder

        fullname = f"{full_base_folder}/{relative_filename}"
        if os.path.exists(fullname):
            os.remove(fullname)

    def _do_remove_file_from_db(self, relative_filename):
        relative_dir = os.path.dirname(relative_filename)
        basename = os.path.basename(relative_filename)
        image_metas = self.db_session.query(ImageMeta).filter(
            and_(ImageMeta.folder == relative_dir, ImageMeta.filename == basename)).all()

        if len(image_metas) > 1:
            raise MultiFileError()

        image_meta = image_metas[0]
        self.db_session.delete(image_meta)


class ActionExecutorList(object):

    def __init__(self, base_folder: str, db_session, actions: list):
        """
        :param base_folder:
        :param db_session: a sqlalchemy session
        :param action_contents: a action list
        example:
          [{"action": "remove_file", "files": ["file2:, "files4"]}

        allow action:
          {"action": "remove_file", "files": ["file2:, "files4"]}
          {"action": "move_file", "from": "file1", "to": "file2"}
        """
        self.base_folder = base_folder
        self.db_session = db_session
        self.actions = actions

    def do(self):
        for action_item in self.actions:
            executor = self._create_executor(action_item)
            executor.do()

    def _create_executor(self, action_item) -> ActionExecutor:
        if action_item["action"] == "remove_file":
            return ActionRemoveFile(self.base_folder, self.db_session, action_item)
        else:
            raise NotImplementedError("unsupported error")
