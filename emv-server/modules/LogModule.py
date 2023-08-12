from time import time

_start_time = time()

def log_info(data):
    global _start_time
    with open("server.log", "a") as f:
        print("{0}s [INFO]: {1}".format(round(time() - _start_time), data), file=f)

def log_warn(data):
    global _start_time
    with open("server.log", "a") as f:
        print("{0}s [WARN]: {1}".format(round(time() - _start_time), data), file=f)

def start_time():
    global _start_time
    return _start_time