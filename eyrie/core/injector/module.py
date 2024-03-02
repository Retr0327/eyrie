from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
import inspect
from types import FunctionType
from typing import TYPE_CHECKING
from uuid import uuid4

from eyrie.common.constants import Watermark
from eyrie.core.errors import RuntimeException
from eyrie.core.utils import get_provider_token

if TYPE_CHECKING:
    from eyrie.common.interfaces.modules import ProviderConfig


@dataclass(slots=True)
class Module:
    _id: str = field(default_factory=lambda: str(uuid4()))
    _name: str = None
    _imports: set = field(default_factory=set)
    _middlewares: dict = field(default_factory=dict)
    _providers: dict = field(default_factory=dict)
    _controllers: dict = field(default_factory=dict)
    _guards: dict = field(default_factory=dict)
    _exports: set = field(default_factory=set)
    _global: bool = False

    def __hash__(self):
        return hash(self._id)

    def add_import(self, import_module: Module):
        self._imports.add(import_module)

    def add_guards(self, guard: type | FunctionType):
        self._guards[guard] = {
            "token": guard,
            "name": get_provider_token(guard),
            "host": self._id,
        }

    def add_middleware(self, middleware: type | FunctionType):
        self._middlewares[middleware] = {
            "token": middleware,
            "name": get_provider_token(middleware),
            "host": self._id,
        }

    def add_provider(self, provider: type | ProviderConfig):
        if not isinstance(provider, dict):
            self._providers[provider] = {
                "token": provider,
                "name": get_provider_token(provider),
                "host": self._id,
                "scope": "singleton",
            }
            return

        inject = provider.get("inject", [])
        provider_cls = inject[0] if inject else provider["provide"]
        config = {
            "token": provider_cls,
            "name": get_provider_token(provider["provide"]),
            "host": self._id,
            "scope": provider.get("scope", "singleton"),
        }
        if len(inject) == 2:
            config["custom_deps"] = inject[-1]

        self._providers[provider_cls] = config

    def add_controller(self, controller: type | FunctionType):
        is_valid = any(isinstance(controller, t) for t in (type, FunctionType))
        if not is_valid:
            name = get_provider_token(controller)
            raise RuntimeException(f"Controller {name} must be a callable or a class")

        self._controllers[controller] = {
            "token": controller,
            "name": get_provider_token(controller),
            "host": self._id,
        }

    def add_export(self, provider: type | FunctionType | ProviderConfig):
        if not isinstance(provider, dict):
            return self._exports.add(provider)

        inject = provider.get("inject", [])
        provider_cls = inject[0] if inject else provider["provide"]
        self._exports.add(provider_cls)

    def build(self, module_map: dict[str, dict[str, type | Module]]):
        metadata = module_map[self._id]["metadata"]
        for provider in metadata.providers:
            self.add_provider(provider)

        for export in metadata.exports:
            self.add_export(export)

        for import_module in metadata.imports:
            module = module_map[import_module.id]["module"]
            self.add_import(module)

        guards = []
        for controller in metadata.controllers:
            controller_guards = getattr(controller, Watermark.GUARDS, [])
            for guard in controller_guards:
                if guard not in guards:
                    guards.append(guard)
            methods = inspect.getmembers(controller, inspect.isfunction)
            for method in methods:
                if hasattr(method, "method"):
                    method_guards = getattr(method, Watermark.GUARDS, [])
                    for guard in method_guards:
                        if guard not in guards:
                            guards.append(guard)

            self.add_controller(controller)

        for guard in guards:
            self.add_guards(guard)

        middleware_metadata = module_map[self._id].get("middlewares", [])
        middlewares = []
        for middleware_info in middleware_metadata:
            middlewares.extend(middleware_info["middlewares"])
        for middleware in list(set(middlewares)):
            self.add_middleware(middleware)
