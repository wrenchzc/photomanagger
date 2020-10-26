import os
import time
import shutil
import pytest
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME, PATH_SEP
from photomanager.db.dbutils import IndexDBRaw, get_db_session, close_db_session
from photomanager.db.models import ImageMeta
from photomanager.db.imagehandler import ImageDBHandler
from photomanager.imageutils import get_folder_image_files
from photomanager.pmconst import PMDBNAME
from photomanager.db.config import Config
from tests.utils import remove_file


@pytest.fixture("function")
def image_handler():
    session = get_db_session(PMDBNAME)
    return ImageDBHandler(".", session, False)


cmd_inx_test_root = 'tests/data'


class TestIndexDB(object):
    @staticmethod
    def _clear():
        db_name = cmd_inx_test_root + '/' + PMDBNAME
        remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
        remove_file(cmd_inx_test_root + '/' + "test_new.jpg")
        if os.path.exists(db_name):
            session = get_db_session(db_name)
            close_db_session(session)
            os.remove(db_name)

    def setup_method(self):
        self._clear()

    def teardown_method(self):
        self._clear()

    def test_option_todo_index(self, image_handler):
        image_handler.do_index([])
        image_handler.todo_index = 129
        assert image_handler.todo_index == 129
        image_handler.todo_index = 139
        assert image_handler.todo_index == 139

    def test_single_image(self, image_handler):
        files = ["tests/data/test1.jpg", "tests/data/test4.jpg"]
        image_handler.do_index(files)
        query = image_handler.session.query(ImageMeta)
        image_metas = query.all()

        assert len(image_metas) == 2
        assert image_metas[0].id == 1
        assert image_metas[0].folder == u'tests/data'
        assert image_metas[0].filename == u'test1.jpg'
        assert image_metas[0].image_width == 1200
        assert image_metas[0].image_height == 1600
        assert image_metas[1].id == 2
        assert image_metas[1].folder == u'tests/data'
        assert image_metas[1].filename == u'test4.jpg'
        assert image_metas[1].image_width == 1057
        assert image_metas[1].image_height == 1123

    def test_folder_files(self):
        files = get_folder_image_files('tests/data')
        assert len(files) == 8
        assert "noexif.jpg" in files
        assert "subdir/dlrb.jpg" in files

    def test_option_values(self, image_handler):
        session = get_db_session(PMDBNAME)
        config = Config(session)
        value = config.get_value("NO_FIELD")
        assert value is None

        config.set_value("TEST_FIELD", "test")
        value = config.get_value("TEST_FIELD")
        assert value == "test"

    def test_image_modified(self, image_handler):
        shutil.copy("tests/data/test1modified", "tests/data/test1.jpg")
        try:
            files = ["tests/data/test1.jpg"]
            image_handler.do_index(files)
            query = image_handler.session.query(ImageMeta)
            image_metas = query.all()
            assert len(image_metas) == 2
            assert image_metas[0].id == 1
            assert image_metas[0].folder == u'tests/data'
            assert image_metas[0].filename == u'test1.jpg'
            assert image_metas[0].image_width == 1200
            assert image_metas[0].image_height == 1600
        finally:
            shutil.copy("tests/data/test1bak", "tests/data/test1.jpg")

    def _do_init_db(self):
        self._clear()

        inx_db = IndexDBRaw(cmd_inx_test_root)
        query_sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table_name}'".format(
            table_name="tbl_images")
        values = inx_db.query(query_sql)
        return values

    def test_init_db(self):
        values = self._do_init_db()
        assert values[0] == (1,)
        values = self._do_init_db()
        assert values[0] == (1,)
