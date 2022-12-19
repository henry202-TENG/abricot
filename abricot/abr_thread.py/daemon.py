import threading

def thread_a_func(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()