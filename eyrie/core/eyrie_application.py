from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import TYPE_CHECKING

from fastapi import Depends

from eyrie.common.interfaces import CanActivate
from eyrie.common.interfaces.middlewares import EyrieGlobalMiddleware

from .injector import EyrieContainer
from .router import RouterFactory
from .scanner import DependenciesScanner
from .utils import (
    sanitize_path,
    should_apply_middleware,
)

if TYPE_CHECKING:
    from fastapi import FastAPI
    from fastapi.routing import APIRoute

    from eyrie.core.injector import Module


@dataclass(slots=True)
class EyrieApplication:
    module_map: dict
    http_server: FastAPI
    global_prefix: str | None = None
    container_context: set = field(default_factory=set)

    def _aggregate_module_components(self, modules: list[Module]):
        providers, controllers = {}, {}
        for module in modules:
            providers.update(module._providers)
            controllers.update(module._controllers)
        return providers, controllers

    def add_global_middlewares(self, *middlewares: EyrieGlobalMiddleware | dict):
        for middleware in middlewares:
            if isinstance(middleware, dict):
                self.http_server.add_middleware(**middleware)
            elif issubclass(middleware, EyrieGlobalMiddleware):
                self.http_server.add_middleware(middleware)
            else:
                self.http_server.add_middleware(*middleware)

    def set_global_prefix(self, prefix: str):
        self.global_prefix = sanitize_path(None, prefix)

    def _register_providers(
        self, modules: list[Module], container: EyrieContainer, providers: dict
    ):
        DependenciesScanner(modules=modules, providers=providers).scan()
        resolved_providers = container.get_resolved_providers(providers)
        for provider in resolved_providers:
            container.add_provider(providers[provider])

    def _build_api_routers(self, controllers: dict):
        routers = []
        for controller in controllers:
            self.container_context.add(controller.__module__)
            if not isinstance(controller, type):
                continue
            router = RouterFactory(
                controller=controller, global_prefix=self.global_prefix
            ).create()

            controller_guards = getattr(controller, "__guards__", [])
            for route in router.router.routes:
                for guard in controller_guards:
                    self.container_context.add(guard.__module__)
                    deps = getattr(route, "dependencies", [])
                    if isinstance(guard, type):
                        if issubclass(guard, CanActivate) or hasattr(
                            guard, "can_activate"
                        ):
                            deps.append(Depends(guard().can_activate))
                        else:
                            deps.append(Depends(guard()))
                    else:
                        deps.append(Depends(guard))

                method_guards = getattr(route.endpoint, "__guards__", [])
                for method_guard in method_guards:
                    self.container_context.add(method_guard.__module__)
                    deps = getattr(route, "dependencies", [])
                    if isinstance(guard, type):
                        if issubclass(guard, CanActivate) or hasattr(
                            guard, "can_activate"
                        ):
                            deps.append(Depends(guard().can_activate))
                        else:
                            deps.append(Depends(guard()))
                    else:
                        deps.append(Depends(guard))

            routers.append(router.router)
        return routers

    def _build_api_middlewares(self, routes: list[APIRoute]):
        middleware_info_list = []
        module_middlewares = list(
            map(lambda value: value.get("middlewares"), self.module_map.values())
        )
        for module_middleware in module_middlewares:
            if module_middleware:
                for item in module_middleware:
                    if item not in middleware_info_list:
                        middleware_info_list.append(item)

        for route in routes:
            for middleware_info in middleware_info_list:
                middlewares = middleware_info.get("middlewares", [])
                methods = list(route.methods)
                for method in methods:
                    should_apply = should_apply_middleware(
                        method, route.path, middleware_info
                    )
                    for middleware in middlewares:
                        self.container_context.add(middleware.__module__)
                        if should_apply:
                            deps = getattr(route, "dependencies", [])
                            deps.append(Depends(middleware()))

    def start(self):
        modules = list(map(lambda value: value["module"], self.module_map.values()))
        container = EyrieContainer()
        providers, controllers = self._aggregate_module_components(modules)
        self._register_providers(modules, container, providers)
        routers = self._build_api_routers(controllers)
        routes = []
        for router in routers:
            routes.extend(router.routes)

        self._build_api_middlewares(routes)
        for router in routers:
            self.http_server.include_router(router)

        container.wire(modules=self.container_context)
        self.http_server.container = container
        return self.http_server
