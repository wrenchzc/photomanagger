import shutil
import time
import os
import pytest
from tests.utils import remove_file
from sqlalchemy import and_
from photomanager.lib.pmconst import PM_TODO_LIST, PMDBNAME
from photomanager.commands.index import CommandIndex
from photomanager.commands.display import CommandList
from photomanager.db.dbutils import get_db_session, close_db_session
from photomanager.controller.controller_file_dup import RemoveDupFilesDoer
from photomanager.lib import errors
from photomanager.db.models import ImageMeta

cmd_inx_test_root = 'tests/data'
default_backup_dir = cmd_inx_test_root + "/../photomanager_backup"


class TestDisplayImg(object):

    @classmethod
    def setup_class(cls):
        cls._clear()
        cls._do_index()

    @classmethod
    def teardown_class(cls):
        cls._clear()
        db_filename = cmd_inx_test_root + '/' + PMDBNAME
        remove_file(db_filename)

    @staticmethod
    def _clear():
        db_filename = cmd_inx_test_root + '/' + PMDBNAME
        close_db_session(db_filename)

    @staticmethod
    def _do_index():
        command_index = CommandIndex(cmd_inx_test_root, {})
        cnt = command_index.do()

    def setup_method(self):
        self._clear()

    def teardown_method(self):
        self._clear()


    def test_date_filter_single(self):
        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.eq:2016-08-05"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 1)
        image_info = image_infos[0]
        assert image_info["filename"] == "test3.jpg"

        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.eq:2016-08-06"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 0)

        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.lt:2016-08-05"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 1)
        image_info = image_infos[0]
        assert image_info["filename"] == "test1.jpg"

        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.lte:2016-08-05"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 2)
        image_info = image_infos[0]
        assert image_info["filename"] == "test1.jpg"
        assert image_infos[1]["filename"] == "test3.jpg"

        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.gt:2016-08-05"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 1)
        image_info = image_infos[0]
        assert image_info["filename"] == "test2.jpg"

        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.gte:2016-08-05"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 2)
        image_info = image_infos[0]
        assert image_info["filename"] == "test2.jpg"
        assert image_infos[1]["filename"] == "test3.jpg"

    def test_date_filter_multi(self):
        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.lt:2016-08-06", "date.gt:2016-08-04"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 1)
        image_info = image_infos[0]
        assert image_info["filename"] == "test3.jpg"


    def test_date_filter_by_file_createtime(self):
        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.eq:2019-02-28"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 2)
        assert image_infos[0]["filename"] == "noexif.jpg"
        assert image_infos[1]["filename"] == "dlrb.jpg"

    def test_date_filter_by_8digit(self):
        command_list = CommandList(cmd_inx_test_root, {"filters": ["date.eq:20160805"]})
        image_infos = command_list.get_filter_images()
        assert (len(image_infos) == 1)
        assert image_infos[0]["filename"] == "test3.jpg"
