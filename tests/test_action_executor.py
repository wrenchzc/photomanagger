from photomanager.utils.action_executor import ActionExecutorList

import shutil
import time
import os
from sqlalchemy import and_
from tests.utils import remove_file, remove_tmp_files
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME, PATH_SEP
from photomanager.commands.index import CommandIndex
from photomanager.db.dbutils import get_db_session
from photomanager.utils.action_executor import ActionRemoveFile
from photomanager.db.models import ImageMeta

cmd_inx_test_root = 'tests/data'


class TestActionExecutor(object):
    db_session = None

    @staticmethod
    def _clear():
        remove_tmp_files(cmd_inx_test_root)

    @staticmethod
    def _copy_dup_files():
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg",
                    f"{cmd_inx_test_root}/test4_dup.jpg")
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg",
                    f"{cmd_inx_test_root}/subdir/test4_dup.jpg")
        time.sleep(0.5)

    @staticmethod
    def _do_index():
        command_index = CommandIndex(cmd_inx_test_root, {})
        cnt = command_index.do()

    # @classmethod
    # def setup_class(cls):
    #    remove_file(cmd_inx_test_root + '/' + PMDBNAME)
    #    cls._copy_dup_files()
    #    cls._do_index()

    # @classmethod
    # def teardown_class(cls):
    #    cls._clear()
    #    remove_file(cmd_inx_test_root + '/' + PMDBNAME)

    def setup_method(self):
        self._clear()
        time.sleep(0.5)
        remove_file(cmd_inx_test_root + '/' + PMDBNAME)
        self._copy_dup_files()
        self._do_index()

    def teardown_method(self):
        self._clear()
        time.sleep(0.5)
        remove_file(cmd_inx_test_root + '/' + PMDBNAME)

    def test_remove_action(self):
        db_session = get_db_session(cmd_inx_test_root + PATH_SEP + PMDBNAME)
        remove_action = dict(action="remove_file", files=["test4_dup.jpg"])
        remove_executor = ActionRemoveFile(
            cmd_inx_test_root, db_session, remove_action)
        remove_executor.do()
        assert (not os.path.exists("tset4_dup.jpg"))
        imgs = db_session.query(ImageMeta).filter(
            and_(ImageMeta.folder == "", ImageMeta.filename == "tset4_dup.jpg")).all()
        assert(len(imgs) == 0)

        remove_action = dict(action="remove_file", files=[
                             "subdir/test4_dup.jpg"])
        remove_executor = ActionRemoveFile(
            cmd_inx_test_root, db_session, remove_action)
        remove_executor.do()
        assert (not os.path.exists("subdir/test4_dup.jpg"))
        imgs = db_session.query(ImageMeta).filter(
            and_(ImageMeta.folder == "subdir", ImageMeta.filename == "tset4_dup.jpg")).all()

    def test_remove_batch(self):
        db_session = get_db_session(cmd_inx_test_root + PATH_SEP + PMDBNAME)
        remove_action1 = dict(action="remove_file", files=["test4_dup.jpg"])
        remove_action2 = dict(action="remove_file", files=[
                              "subdir/test4_dup.jpg"])

        remove_actions = ActionExecutorList(cmd_inx_test_root, db_session, [
                                            remove_action1, remove_action2])
        remove_actions.do()
        assert (not os.path.exists("subdir/test4_dup.jpg"))
        assert (not os.path.exists("tset4_dup.jpg"))
