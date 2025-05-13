from concurrent.futures import ThreadPoolExecutor
from functools import wraps

_executor = ThreadPoolExecutor(max_workers=4)

def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _executor.submit(func, *args, **kwargs)
    return wrapper
