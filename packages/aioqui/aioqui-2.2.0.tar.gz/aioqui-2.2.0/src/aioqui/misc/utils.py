from functools import cache, wraps
from typing import Awaitable, Any, Callable


class CachedAwaitable:
    def __init__(self, awaitable: Awaitable):
        self.awaitable: Awaitable = awaitable
        self.result: Any = None

    def __await__(self) -> Any:
        if not self.result:
            self.result = yield from self.awaitable.__await__()
        return self.result


def reawaitable(func: Callable, /):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return CachedAwaitable(func(*args, **kwargs))
    return wrapper


def aiocache(func: Callable, /):
    return cache(reawaitable(func))