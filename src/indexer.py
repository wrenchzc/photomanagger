import os
from exceptions import IOError


def index_image(folder, force=False):
    folder = os.path.expanduser(folder)
    if not os.path.exists(folder):
        raise IOError("folder {folder} does not existed".format(folder))
