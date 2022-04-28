from functools import wraps


def header(key: str, value: str):
    def decorator(func):
        @wraps(func)
        def wrap(self, *args,**kwargs):
            self.header[key] = value
            return func(self, *args, **kwargs)
        return wrap
    return decorator