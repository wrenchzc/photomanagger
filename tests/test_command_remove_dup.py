import shutil
import time
import os
from tests.utils import remove_file
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME
from photomanager.commands.index import CommandIndex
from photomanager.db.dbutils import get_db_session
from photomanager.utils.remove_dup_doer import RemoveDupInOneFolderExecuter

cmd_inx_test_root = 'tests/data'


class TestRemoveDup(object):
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

    def test_remove_dup_one_folder(self):
        db_session = get_db_session(cmd_inx_test_root + os.path.sep + PMDBNAME)
        executor = RemoveDupInOneFolderExecuter(cmd_inx_test_root, db_session, '')
        dup_files = executor.get_dupfile_list()
        keys = list(dup_files.keys())
        assert len(keys) == 1
        assert len(dup_files[keys[0]]) == 2
        assert dup_files[keys[0]] == ["test4.jpg", "test4_dup.jpg"]

        action_list = executor.generate_action_list(dup_files)
        assert len(action_list) == 1
        action = action_list[0]
        assert action["action"] == "remove_file"
        assert action["files"] == ["test4_dup.jpg"]
