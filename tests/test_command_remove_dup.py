import shutil
import time
from tests.utils import remove_file
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME, PATH_SEP
from photomanager.commands.index import CommandIndex
from photomanager.db.dbutils import get_db_session
from photomanager.utils.remove_dup_doer import RemoveDupInOneFolderExecutor

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
        db_session = get_db_session(cmd_inx_test_root + PATH_SEP + PMDBNAME)
        executor = RemoveDupInOneFolderExecutor(cmd_inx_test_root, db_session, '')
        dup_files = executor.get_dupfile_list()
        keys = list(dup_files.keys())
        assert len(keys) == 1
        dup_files_by_md5_1 = dup_files[keys[0]]
        assert len(dup_files_by_md5_1) == 2
        assert set(dup_files_by_md5_1).difference(set(["test4.jpg", "test4_dup.jpg"])) == set([])

        action_list = executor.generate_action_list(dup_files)
        assert len(action_list) == 1
        action = action_list[0]
        assert action["action"] == "remove_file"
        assert action["files"] == [dup_files_by_md5_1[1]]
