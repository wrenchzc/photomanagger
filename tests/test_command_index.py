import os
from src.commands.index import CommandIndex
from src.pmconst import PM_TODO_INDEX, PM_TODO_LIST

def _clear():
    if os.path.exists('data/' + PM_TODO_LIST):
        os.remove('data/' + PM_TODO_LIST)
    if os.path.exists('data/' + PM_TODO_INDEX):
        os.remove('data/' + PM_TODO_INDEX)


def test_todolist_and_resume():
    _clear()
    try:
        command_index = CommandIndex('data', {})
        command_index.get_file_list()
        assert len(command_index.file_list) == 6
        assert command_index.todo_inx == 0
        command_index.get_file_list()
        assert len(command_index.file_list) == 6
        assert command_index.todo_inx == 0

        f = open("data/" + PM_TODO_INDEX, "w")
        f.write("3")
        f.close()

        command_index.get_file_list()
        assert len(command_index.file_list) == 6
        assert command_index.todo_inx == 3
    finally:
        _clear()


