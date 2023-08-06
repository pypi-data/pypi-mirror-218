import time
from datetime import datetime

def time_to_str(timestamp=None, f="%Y-%m-%d %H:%M:%S"):
    '''
    Args 
        f - %Y-%m-%d %H:%M:%S 格式化时间
    '''
    if timestamp:
        ts = datetime.fromtimestamp(timestamp)
    else:
        ts = datetime.now()
    formatted = ts.strftime(f)
    return formatted

def str_to_time(date, f="%Y-%m-%d %H:%M:%S"):
    '''
    Args:
        str_date - 字符时间
        f - 默认 %Y-%m-%d %H:%M:%S '''
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def timestamp():
    return time.time()
