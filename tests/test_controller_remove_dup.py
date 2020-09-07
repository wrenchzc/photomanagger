import shutil
import time
import os
import pytest
from tests.utils import remove_file
from sqlalchemy import and_
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME, PATH_SEP
from photomanager.commands.index import CommandIndex
from photomanager.db.dbutils import get_db_session
from photomanager import errors
from photomanager.db.models import ImageMeta
from photomanager.controller.controller_file_dup import FileDupController
from photomanager.commands.remove_dup import CommandRemoveDuplicate

cmd_inx_test_root = 'tests/data'


class TestRemoveDupController(object):
    db_session = None

    @staticmethod
    def _clear():
        remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
        remove_file(cmd_inx_test_root + '/' + "test_new.jpg")
        remove_file(f"{cmd_inx_test_root}/test3_dup.jpg")
        remove_file(f"{cmd_inx_test_root}/test2_dup.jpg")
        remove_file(f"{cmd_inx_test_root}/test4_dup.jpg")
        remove_file(f"{cmd_inx_test_root}/subdir/test4_dup.jpg")

    @staticmethod
    def _copy_dup_files():
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg",
                    f"{cmd_inx_test_root}/test4_dup.jpg")
        shutil.copy(f"{cmd_inx_test_root}/test4.jpg",
                    f"{cmd_inx_test_root}/subdir/test4_dup.jpg")
        shutil.copy(f"{cmd_inx_test_root}/test3.jpg",
                    f"{cmd_inx_test_root}/test3_dup.jpg")
        shutil.copy(f"{cmd_inx_test_root}/test2.jpg",
                    f"{cmd_inx_test_root}/test2_dup.jpg")
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

    def test_controller_nava(self):
        db_session = get_db_session(cmd_inx_test_root + '/' + PMDBNAME)
        cmd_dup = CommandRemoveDuplicate(cmd_inx_test_root, {})
        ui_data = cmd_dup._list_duplicate()
        expect_data = {
                "4a298b2c1e0b9d02550d8f3a32b5b2d3": [("", "test4.jpg"), ("", "test4_dup.jpg"), ("subdir", "test4_dup.jpg")],
                "91eaa1d0d7279b95f2f31b42d5daa57b": [("", "test3.jpg"), ("", "test3_dup.jpg")],
                "f13741794005bc944d2b37f1db2a0775": [("", "test2.jpg"), ("", "test2_dup.jpg")],
                }
        assert ui_data == expect_data

        keys = list(expect_data)
        file_list0 = ["test4.jpg", "test4_dup.jpg", "subdir/test4_dup.jpg"]
        file_list1 = ["test3.jpg", "test3_dup.jpg"]
        file_list2 = ["test2.jpg", "test2_dup.jpg"]
               
        controller = FileDupController(cmd_inx_test_root, db_session, ui_data)
        assert controller.active_index == 0
        assert controller.active_key == keys[0]
        assert controller.current_dup_files == file_list0
        controller.next()
        assert controller.active_index == 1
        assert controller.active_key == keys[1]
        assert controller.current_dup_files == file_list1
        controller.next()
        assert controller.active_index == 2
        assert controller.active_key == keys[2]
        assert controller.current_dup_files == file_list2
        controller.next()
        assert controller.active_index == 2
        controller.prev()
        assert controller.active_index == 1
        controller.prev()
        assert controller.active_index == 0
        controller.prev()
        assert controller.active_index == 0


    def test_controller_delete(self):
        db_session = get_db_session(cmd_inx_test_root + '/' + PMDBNAME)
        cmd_dup = CommandRemoveDuplicate(cmd_inx_test_root, {})
        ui_data = cmd_dup._list_duplicate()
        controller = FileDupController(cmd_inx_test_root, db_session, ui_data)
        keys = list(ui_data)
        file_list0 = ["test4.jpg", "test4_dup.jpg", "subdir/test4_dup.jpg"]
        file_list1 = ["test3.jpg", "test3_dup.jpg"]
        file_list2 = ["test2.jpg", "test2_dup.jpg"]

        controller.active_index = 1
        assert len(controller.dup_keys) == 3
        with pytest.raises(errors.RemoveImageCannotRemoveAllError) as exc_info:
            controller.delete_current_dups_by_indexs([0,1])
        assert exc_info.value.error_code == 40002        
        controller.delete_current_dups_by_indexs([1])
        assert len(controller.dup_keys) == 2
        assert controller.active_index == 1
        assert controller.active_key == keys[2]
        assert controller.current_dup_files == file_list2

        controller.active_index = 0
        controller.delete_current_dups_by_indexs([1])
        assert len(controller.dup_keys) == 2
        assert controller.active_index == 0
        assert controller.active_key == keys[0]
        expect_list = file_list0
        expect_list.pop(1)
        assert controller.current_dup_files == expect_list

        controller.active_index = 1
        controller.delete_current_dups_by_indexs([1])
        assert len(controller.dup_keys) == 1
        assert controller.active_index == 0
        assert controller.active_key == keys[0]
        assert controller.current_dup_files == expect_list


