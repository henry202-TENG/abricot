""" path functions """
from pathlib import Path
import os

def path_win2linux(path: str)-> str:
    """ Make a window path to linux path.

    Args:
        path (str): A window path.

    Returns:
        str: _description_
    """
    if os.name == 'nt':
        path = Path(path).as_posix()
    return path

def path_linux2win(path: str)-> str:
    """ Make a linux path to window path.

    Args:
        path (str): A linux path.

    Returns:
        str: A window path.
    """
    if os.name != 'nt':
        path = path.replace("\\", "/")
    return path
