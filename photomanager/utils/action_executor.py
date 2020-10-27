import os
import platform
import typing
import shutil
from photomanager.db.models import ImageMeta
from sqlalchemy import and_
from sqlalchemy.orm import Session
from photomanager.lib.errors import MultiFileError
from photomanager.lib.pmconst import PATH_SEP
from photomanager.db.config import Config, FieldBackupDir
from photomanager.utils.pathutils import is_abspath


class ActionExecutor(object):

    def __init__(self, base_folder: str, db_session: Session, action_item: typing.Dict[str, typing.List]):
        self.base_folder = base_folder
        self.db_session = db_session
        self.action_item = action_item
        self.config = Config(db_session)

    def do(self):
        raise NotImplementedError


class ActionRemoveFile(ActionExecutor):

    def do(self):
        if self.action_item["action"] != "remove_file":
            raise ValueError

        for relative_file in self.action_item["files"]:
            self.do_remove_file(relative_file)

    def do_remove_file(self, relative_filename):
        self._do_backup_file(relative_filename)
        self._do_remove_file_from_disk(relative_filename)
        self._do_remove_file_from_db(relative_filename)

    def _do_backup_file(self, relative_filename):
        full_name = self._get_fullname(relative_filename)
        if not os.path.exists(full_name):
            return

        backup_dir = self.config.get_value(FieldBackupDir)
        if not is_abspath(backup_dir):
            backup_dir = self.base_folder + PATH_SEP + backup_dir

        # remove driver letter
        if platform.system() == "Windows" and not self.base_folder[1] == ":":
            relative_filename = relative_filename[2:]

        # remove first path separator
        if relative_filename[0] == PATH_SEP:
            relative_filename = relative_filename[1:]

        backup_filename = f"{backup_dir}{PATH_SEP}{relative_filename}"
        backup_file_path, _ = os.path.split(backup_filename)
        os.makedirs(backup_file_path, exist_ok=True)

        if os.path.exists(backup_filename):
            ori_backup_name = backup_filename
            for i in range(10000):
                if not os.path.exists(f"{ori_backup_name}.{i}"):
                    backup_filename = f"{ori_backup_name}.{i}"
                    break
        shutil.copyfile(full_name, backup_filename)

    def _get_fullname(self, relative_filename: str):
        full_base_folder = self.base_folder
        if platform.system() == "Linux" and not self.base_folder.startswith(PATH_SEP):  # relative path:
            full_base_folder = os.getcwd() + PATH_SEP + self.base_folder
        elif platform.system() == "Windows" and not self.base_folder[1] == ":":
            full_base_folder = os.getcwd() + PATH_SEP + self.base_folder

        return f"{full_base_folder}/{relative_filename}"

    def _do_remove_file_from_disk(self, relative_filename: str):
        fullname = self._get_fullname(relative_filename)
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
