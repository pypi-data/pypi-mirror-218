class PipeFunc:
    def __init__(self, func):
        self.func = func

    def __ror__(self, iterable):
        return self.func(iterable)


def piped(func):
    def wrapper(*args, **kwargs):
        return PipeFunc(lambda iterable: func(iterable, *args, **kwargs))
    return wrapper


def pipable(func):
    def helper(iterable, *args, **kwargs):
        for line in iterable:
            yield func(line, *args, **kwargs)

    return piped(helper)
