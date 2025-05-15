from typing import TypeVar, Callable, Coroutine, Any

T = TypeVar('T')
Coro = Coroutine[Any, Any, T]
AsyncFunc = TypeVar("AsyncFunc", bound=Callable[..., Coro[Any]])

def original(obj: object):
    return obj