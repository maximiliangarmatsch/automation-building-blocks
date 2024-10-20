import os


def is_osx():
    if os.uname().sysname == "Darwin":
        return True
    return False
