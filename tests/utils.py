import os


def remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError as e:
            error_message = str(e)
            print(f"remove '{filename}' failed, message is {error_message}")