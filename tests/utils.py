import os


def remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            pass