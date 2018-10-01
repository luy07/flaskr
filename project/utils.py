import time
def get_formatted_localtime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())