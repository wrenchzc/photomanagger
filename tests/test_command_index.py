import os
from src.commands.index import CommandIndex
from src.pmconst import PM_TODO_LIST, PMDBNAME

cmd_inx_test_root = 'tests/data'


def _remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def _clear():
    _remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
    _remove_file(cmd_inx_test_root + '/' + PMDBNAME)


def setup_function():
    _clear()


def teardown_function():
    _clear()


def test_todolist_and_resume():
    command_index = CommandIndex(cmd_inx_test_root, {})
    command_index.get_file_list()
    assert len(command_index.file_list) == 6
    assert command_index.todo_inx == 0
    command_index.get_file_list()
    assert len(command_index.file_list) == 6
    assert command_index.todo_inx == 0

    command_index.handler.todo_index = 3

    command_index.get_file_list()
    assert len(command_index.file_list) == 6
    assert command_index.todo_inx == 3


def test_wrong_todo_inx():
    command_index = CommandIndex(cmd_inx_test_root, {})
    command_index.handler.todo_index = 0
    command_index.get_file_list()
    assert len(command_index.file_list) == 6


def test_command_index():
    command_index = CommandIndex(cmd_inx_test_root, {})
    command_index.do()
