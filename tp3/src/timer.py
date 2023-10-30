import time as tm

Time = float
Length = float


def timer(f):
    def new_f(file_name):
        start = tm.time()
        path, length = f(file_name)
        end = tm.time()
        time = end-start
        return path, length, time
    return new_f
