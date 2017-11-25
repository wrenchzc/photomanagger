import time
import hashlib


def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def get_file_md5(filename):
    with open(filename, "rb") as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()