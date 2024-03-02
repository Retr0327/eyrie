from typing import (
    Any,
    Callable,
    TypeVar,
)

from dependency_injector.wiring import inject as _inject

F = TypeVar("F", bound=Callable[..., Any])


def Inject(fn: F) -> F:
    "Decorator that marks a constructor parameter as a target for [Dependency Injection (DI)](https://python-dependency-injector.ets-labs.org/index.html)."
    return _inject(fn)
