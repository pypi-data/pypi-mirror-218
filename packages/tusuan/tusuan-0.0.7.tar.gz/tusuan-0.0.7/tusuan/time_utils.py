from datetime import datetime


def nowstr():
    return datetime.now().strftime("%Y%m%d%H%M%S")

