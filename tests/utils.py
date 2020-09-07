import os
from photomanager.pmconst import PM_TODO_LIST


def remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError as e:
            error_message = str(e)
            print(f"remove '{filename}' failed, message is {error_message}")


def remove_tmp_files(cmd_inx_test_root):
    import time
    time.sleep(0.2)
    remove_file(cmd_inx_test_root + '/' + PM_TODO_LIST)
    remove_file(cmd_inx_test_root + '/' + "test_new.jpg")
    remove_file(f"{cmd_inx_test_root}/test3_dup.jpg")
    remove_file(f"{cmd_inx_test_root}/test2_dup.jpg")
    remove_file(f"{cmd_inx_test_root}/test4_dup.jpg")
    remove_file(f"{cmd_inx_test_root}/subdir/test4_dup.jpg")
