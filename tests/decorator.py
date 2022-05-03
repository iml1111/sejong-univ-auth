"""
Test Decorator
"""
from functools import wraps
from time import time

def timer(func):
    """Timer"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_time = time()
        result = func(*args, **kwargs)
        sec = time() - process_time
        print("sec:", round(sec, 5))
        return result
    return wrapper