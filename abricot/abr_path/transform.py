from pathlib import Path
import os

def path_win2linux(path):
    if os.name == 'nt':
        path = Path(path).as_posix()
    return path

def path_linux2win(path):
    if os.name != 'nt':
        path = path.replace("\\", "/")
    return path