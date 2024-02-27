from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import (
    Any,
    TypedDict,
)

if TYPE_CHECKING:
    from eyrie.common.enums import RequestMethod


class RouteInfo(TypedDict):
    path: str
    method: RequestMethod


class MiddlewareConfiguration(TypedDict):
    middleware: Any
    forRoutes: list[Any | str | RouteInfo]
