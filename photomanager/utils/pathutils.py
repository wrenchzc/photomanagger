from photomanager.lib.pmconst import PATH_SEP


def is_abspath(path):
    return path[0] == PATH_SEP or (len(path) > 1 and path[1] == ":")
