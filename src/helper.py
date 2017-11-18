import time


def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
