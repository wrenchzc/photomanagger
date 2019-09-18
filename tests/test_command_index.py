import os
import shutil
from photomanager.commands.index import CommandIndex
from photomanager.pmconst import PM_TODO_LIST, PMDBNAME
from photomanager.db.models import ImageMeta

cmd_inx_test_root = 'tests/data'
TEST_FILE_COUNT = 8


def _remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            pass


def _clear():
    _remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
    _remove_file(cmd_inx_test_root + '/' + PMDBNAME)
    _remove_file(cmd_inx_test_root + '/' + "test_new.jpg")


def setup_function():
    _clear()


def teardown_function():
    _clear()


def test_todolist_and_resume():
    command_index = CommandIndex(cmd_inx_test_root, {})
    command_index.get_file_list()
    assert len(command_index.file_list) == TEST_FILE_COUNT
    assert command_index.todo_inx == 0
    command_index.get_file_list()
    assert len(command_index.file_list) == TEST_FILE_COUNT
    assert command_index.todo_inx == 0

    command_index.handler.todo_index = 3

    command_index.get_file_list()
    assert len(command_index.file_list) == TEST_FILE_COUNT
    assert command_index.todo_inx == 3


def test_wrong_todo_inx():
    command_index = CommandIndex(cmd_inx_test_root, {})
    command_index.handler.todo_index = 0
    command_index.get_file_list()
    assert len(command_index.file_list) == TEST_FILE_COUNT


def test_command_index():
    command_index = CommandIndex(cmd_inx_test_root, {})
    cnt = command_index.do()
    assert command_index.handler.todo_index == -1
    assert not os.path.exists(command_index.todo_file_name)
    assert command_index.handler.session.query(ImageMeta).count() == TEST_FILE_COUNT
    assert cnt[0] == TEST_FILE_COUNT

    command_index = CommandIndex(cmd_inx_test_root, {})
    cnt = command_index.do()
    assert command_index.handler.todo_index == -1
    assert not os.path.exists(command_index.todo_file_name)
    assert command_index.handler.session.query(ImageMeta).count() == TEST_FILE_COUNT
    assert cnt[0] == 0

    shutil.copy(cmd_inx_test_root + "/test1.jpg", cmd_inx_test_root + "/test_new.jpg")
    command_index = CommandIndex(cmd_inx_test_root, {})
    cnt = command_index.do()
    assert command_index.handler.todo_index == -1
    assert not os.path.exists(command_index.todo_file_name)
    assert command_index.handler.session.query(ImageMeta).count() == TEST_FILE_COUNT + 1
    assert cnt[0] == 1

    os.remove(cmd_inx_test_root + "/test_new.jpg")
    command_index = CommandIndex(cmd_inx_test_root, {"clean": True})
    cnt = command_index.do()
    assert command_index.handler.todo_index == -1
    assert not os.path.exists(command_index.todo_file_name)
    assert command_index.handler.session.query(ImageMeta).count() == TEST_FILE_COUNT
    assert cnt[1] == 1
