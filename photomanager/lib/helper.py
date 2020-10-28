import time
import hashlib


def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_timestamp_from_str(time_str: str) -> float:
    try:
        time_stamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        time_stamp = 0
    except TypeError:
        time_stamp = 0
    return time_stamp


def get_file_md5(filename):
    with open(filename, "rb") as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()
