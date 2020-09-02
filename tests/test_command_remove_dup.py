import shutil
import time
import os
import pytest
from tests.utils import remove_file
from sqlalchemy import and_
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME, PATH_SEP
from photomanager.commands.index import CommandIndex 
from photomanager.commands.remove_dup import CommandRemoveDuplicate
from photomanager.db.dbutils import get_db_session
from photomanager.utils.remove_dup_doer import RemoveDupFilesController
from photomanager import errors
from photomanager.db.models import ImageMeta

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

    def test_list_dup(self):
        cmd_dup = CommandRemoveDuplicate(cmd_inx_test_root, {})
        dup_list = cmd_dup._list_duplicate()
        expect_data = {
         '4a298b2c1e0b9d02550d8f3a32b5b2d3':  [('', 'test4.jpg'), ('', 'test4_dup.jpg'), ('subdir', 'test4_dup.jpg')]
        }
        assert(dup_list == expect_data)


    def test_remove_dups_error(self):
        dup_files = [('', 'test4.jpg'), ('', 'test4_dup.jpg'), ('subdir', 'test4_dup.jpg')]
        db_session = get_db_session(cmd_inx_test_root + '/' + PMDBNAME)
        remove_dup_ctr = RemoveDupFilesController(cmd_inx_test_root, db_session, dup_files)
        with pytest.raises(errors.RemoveImageIndexOutofRangeError) as exc_info:
            remove_dup_ctr.delete([-1])
        assert exc_info.value.error_code == 40001
        with pytest.raises(errors.RemoveImageCannotRemoveAllError) as exc_info:
            remove_dup_ctr.delete([0, 1, 2])
        assert exc_info.value.error_code == 40002


    def test_remove_dups(self):
        dup_files = [('', 'test4.jpg'), ('', 'test4_dup.jpg'), ('subdir', 'test4_dup.jpg')]
        db_session = get_db_session(cmd_inx_test_root + '/' + PMDBNAME)
        remove_dup_ctr = RemoveDupFilesController(cmd_inx_test_root, db_session, dup_files)
        cnt = remove_dup_ctr.delete([1,2])
        assert(cnt == 2)
        assert (not os.path.exists(cmd_inx_test_root +  "/subdir/test4_dup.jpg"))
        assert (not os.path.exists(cmd_inx_test_root + "/test4_dup.jpg"))
        assert (os.path.exists(cmd_inx_test_root + "/test4.jpg"))
        imgs = db_session.query(ImageMeta).filter(
            and_(ImageMeta.folder == "subdir", ImageMeta.filename == "tset4_dup.jpg")).all()
        assert len(imgs) == 0


