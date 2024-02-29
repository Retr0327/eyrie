from __future__ import annotations

from typing import TYPE_CHECKING

from eyrie.common.enums import RequestMethod

if TYPE_CHECKING:
    from eyrie.common.interfaces.middlewares import RouteInfo


def add_leading_slash(path: str = None):
    if path and isinstance(path, str):
        return path if path.startswith("/") else f"/{path}"
    return ""


class RoutesMapper:
    @staticmethod
    def to_route_info_list(route: str | RouteInfo) -> list[RouteInfo]:
        if isinstance(route, str):
            return [{"path": add_leading_slash(route), "method": RequestMethod.ALL}]

        route["path"] = add_leading_slash(route["path"])
        return [route]
