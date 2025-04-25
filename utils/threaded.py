from functools import wraps
from threading import Thread


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper