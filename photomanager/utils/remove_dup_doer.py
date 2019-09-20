from sqlalchemy import func, desc, and_
from photomanager.db.models import ImageMeta
from photomanager.errors import MultiFileError

REMOVE_DUP_MODE_LIST = ["GENERATE_DELETE_LIST", "REAL_DELETE"]


class RemoveDupExecutor(object):

    def __init__(self, base_folder: str, db_session):
        self.base_folder = base_folder
        self.db_session = db_session

    def do(self):
        raise NotImplementedError


class RemoveDupInOneFolderExecutor(RemoveDupExecutor):

    def __init__(self, base_folder, db_session, relative_path: str):
        RemoveDupExecutor.__init__(self, base_folder, db_session)
        self.relative_path = relative_path

    def do(self):
        dup_file_list = self.get_dupfile_list()
        action_mode = self.__get_action_mode()
        self.__do_action(dup_file_list, action_mode)

    def get_dupfile_list(self):
        """
        :return: return a dict
        example:  { "md5_1": ["file1", "file2"], "md5_2": ["file1", "file2"]}
        """
        dup_md5s = self.db_session.query(func.count(ImageMeta.md5), ImageMeta.md5).filter(
            ImageMeta.folder == self.relative_path).group_by(
            ImageMeta.md5).having(
            func.count(ImageMeta.md5) > 1).order_by(desc(func.count(ImageMeta.md5))).all()

        dup_files_dict = {}
        for md5_meta in dup_md5s:
            md5 = md5_meta.md5
            dup_files_by_md5 = self.db_session.query(ImageMeta.filename). \
                filter(and_(ImageMeta.md5 == md5, ImageMeta.folder == self.relative_path)).all()
            dup_files_dict[md5] = [dup_file.filename for dup_file in dup_files_by_md5]

        return dup_files_dict

    def generate_action_list(self, dup_files_by_md5):
        """
        :param dup_files_by_md5: out put of get_dupfile_list
        :return: a action list, each action is a dict, and save as a json file
        example:
          [{"action": "remove_file", "files": ["file2:, "files4"]}
        """

        to_remove_files = []

        for md5 in dup_files_by_md5:
            dup_files = dup_files_by_md5[md5]
            to_remove_files.extend(dup_files[1:])

        action_item = dict(action="remove_file",  files = to_remove_files)
        return [action_item]


    def __get_action_mode(self):
        return "GENERATE_DELETE_LIST"

    def __do_action(self, dup_file_list, action_mode):
        pass
