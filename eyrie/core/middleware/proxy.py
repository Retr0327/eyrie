from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
import re
from typing import TYPE_CHECKING

from eyrie.common.interfaces import MiddlewareConfigProxy

from .mapper import RoutesMapper

if TYPE_CHECKING:
    from collections.abc import Sequence

    from eyrie.common.interfaces import (
        EyrieMiddleware,
        MiddlewareConsumer,
        RouteInfo,
    )

    from .builder import MiddlewareBuilder


@dataclass(slots=True)
class ConfigProxy(MiddlewareConfigProxy):
    builder: MiddlewareBuilder
    middlewares: Sequence[EyrieMiddleware]
    excluded_routes: list[str | RouteInfo | type] = field(default_factory=list)

    def exclude(self, *routes: str | RouteInfo) -> MiddlewareConfigProxy:
        excluded_routes = []
        flatted_routes = self._get_routes_flat_list(routes)
        for route in flatted_routes:
            if route not in excluded_routes:
                excluded_routes.append(route)
        self.excluded_routes.extend(excluded_routes)
        return self

    def for_routes(self, *routes: str | RouteInfo) -> MiddlewareConsumer:
        flatted_routes = self._get_routes_flat_list(routes)
        for_routes = self._remove_overlapped_routes(flatted_routes)
        config = {
            "middlewares": list(self.middlewares),
            "for_routes": for_routes,
            "excluded_routes": self.excluded_routes,
        }
        if config not in self.builder.middleware_collection:
            self.builder.middleware_collection.append(config)
        return self.builder

    def _get_routes_flat_list(self, routes: list[str | RouteInfo | type]):
        route_info_list = []
        for route in routes:
            mapped_route = RoutesMapper.to_route_info_list(route)
            if isinstance(mapped_route, list):
                for item in mapped_route:
                    if item not in route_info_list:
                        route_info_list.append(item)
            else:
                if mapped_route not in route_info_list:
                    route_info_list(mapped_route)
        return route_info_list

    def _remove_overlapped_routes(self, routes: list[RouteInfo]):
        regex_match_params = r"(:[^\/]*)"
        wildcard = r"([^/]*)"
        regex_routes = []
        for route in routes:
            if ":" in route["path"]:
                regex_route = {
                    "path": route["path"],
                    "method": route["method"],
                    "regex": re.compile(
                        f"^{re.sub(regex_match_params, wildcard, route['path'])}$"
                    ),
                }
                regex_routes.append(regex_route)

        filtered_routes = []
        for route in routes:
            if (
                self._is_not_overlapped(route, regex_routes)
                and route not in filtered_routes
            ):
                filtered_routes.append(route)
        return filtered_routes

    def _is_not_overlapped(self, route: RouteInfo, regex_routes: list):
        for regex_route in regex_routes:
            if route["method"] != regex_route["method"]:
                continue
            normalized_path = route["path"].rstrip("/")
            if normalized_path != regex_route["path"] and regex_route["regex"].match(
                normalized_path
            ):
                return False
        return True
