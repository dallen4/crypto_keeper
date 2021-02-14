import time

def get_current_time():
    ms_float = time.time_ns() / 1000000
    return int(ms_float)

MS_IN_HOUR = 3600000
