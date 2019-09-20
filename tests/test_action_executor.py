from photomanager.utils.action_executor import ActionExecutorList

import shutil
import time
import os
from tests.utils import remove_file
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME
from photomanager.commands.index import CommandIndex
from photomanager.db.dbutils import get_db_session
from photomanager.utils.action_executor import ActionRemoveFile

cmd_inx_test_root = 'tests/data'


class TestActionExecutor(object):
    db_session = None

    @staticmethod
    def _clear():
        remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
        remove_file(cmd_inx_test_root + '/' + "test_new.jpg")

    @staticmethod
    def _copy_dup_files():
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg", f"{cmd_inx_test_root}/test4_dup.jpg")
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg", f"{cmd_inx_test_root}/subdir/test4_dup.jpg")
        time.sleep(0.5)

    @staticmethod
    def _do_index():
        command_index = CommandIndex(cmd_inx_test_root, {})
        cnt = command_index.do()

    @classmethod
    def setup_class(cls):
        remove_file(cmd_inx_test_root + '/' + PMDBNAME)
        cls._copy_dup_files()
        cls._do_index()

    @classmethod
    def teardown_class(cls):
        cls._clear()
        remove_file(cmd_inx_test_root + '/' + PMDBNAME)

    def setup_method(self):
        self._clear()

    def teardown_method(self):
        self._clear()

    def test_remove_action(self):
        db_session = get_db_session(cmd_inx_test_root + os.path.sep + PMDBNAME)
        remove_action = dict(action="remove_file", files=["tset4_dup.jpg"])
        remove_executor = ActionRemoveFile(cmd_inx_test_root, db_session, remove_action)
        remove_executor.do()
        assert(os.path.exists("tset4_dup.jpg"))
