from collections.abc import Mapping
import inspect
from types import FunctionType
from typing import (
    Any,
    overload,
)

from eyrie.common.constants import (
    MetaData,
    Watermark,
)


@overload
def Controller() -> type | FunctionType:
    """Decorator that marks a function as a Eyrie controller that can receive inbound
    requests and produce responses.
    """


@overload
def Controller(prefix: str) -> type | FunctionType:
    """Decorator that marks a class as a Eyrie controller that can receive inbound
    requests and produce responses.

    Args:
        prefix (str): string that defines a `route path prefix`. The prefix
        is pre-pended to the path specified in any request decorator in the class.
    """


@overload
def Controller(options: Mapping[str, Any]) -> type | FunctionType:
    """Decorator that marks a class as a Eyrie controller that can receive inbound
    requests and produce responses.

    Args:
        options (str): options that is related to the FastAPI [APIRouter options](https://fastapi.tiangolo.com/reference/apirouter/).
    """


def Controller(arg: str | Mapping[str, Any] | None = None):
    def wrapper(cls: type | FunctionType):
        setattr(cls, Watermark.CONTROLLER, True)
        if inspect.isfunction(cls):
            return cls

        prefix = "/"
        options = {}
        if isinstance(arg, str):
            prefix = arg
        elif isinstance(arg, dict):
            prefix = arg.get("prefix", "/")
            options = arg

        sanitized_path = f"/{prefix.lstrip('/').rstrip('/')}"
        options["prefix"] = sanitized_path
        setattr(cls, MetaData.CONTROLLER_PATH, sanitized_path)
        setattr(cls, MetaData.CONTROLLER_SCOPE, options)
        return cls

    return wrapper
