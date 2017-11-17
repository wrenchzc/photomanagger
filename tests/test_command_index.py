import os
from src.commands.index import CommandIndex
from src.pmconst import PM_TODO_LIST, PMDBNAME



def _remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def _clear():
    _remove_file('tests/data/' + PM_TODO_LIST)
    _remove_file('tests/data/' + PMDBNAME)


def test_todolist_and_resume():
    _clear()
    command_index = CommandIndex('tests/data', {})
    try:
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
    finally:
        command_index.db_session.close()
        _clear()


def test_command_index():
    _clear()
    try:
        command_index = CommandIndex('tests/data', {})
        command_index.do()
    finally:
        _clear()
