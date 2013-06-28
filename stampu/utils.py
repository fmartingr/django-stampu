import os
import errno
from shutil import rmtree


# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_recursive(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise Exception(exc)


def rmdir(path):
    rmtree(path)
