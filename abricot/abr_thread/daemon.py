""" thread """
import threading

def thread_a_func(func, *args):
    """ make a function as daemon.

    Args:
        func (func): The function to be set.
    """
    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()
