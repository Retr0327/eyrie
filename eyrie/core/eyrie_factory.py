from __future__ import annotations

from typing import TYPE_CHECKING

from eyrie.common.constants import MetaData
from eyrie.common.interfaces import EyrieModule

from .errors import ExceptionsZone
from .eyrie_application import EyrieApplication
from .injector import Module
from .metdata_scanner import MetadataScanner
from .middleware import MiddlewareBuilder

if TYPE_CHECKING:
    from fastapi import FastAPI

    from eyrie.common.interfaces import ModuleMetadata


class EyrieFactoryStatic:
    def create(
        self, module: ModuleMetadata | EyrieModule, http_adapter: FastAPI
    ) -> EyrieApplication:
        module_map = self._build_module_map(module)
        self._initialize(module_map)
        instance = EyrieApplication(module_map=module_map, http_server=http_adapter)
        return instance

    def _initialize(self, module_map: dict[str, dict[str, type | Module]]):
        for module_info in module_map.values():
            metadata_scanner = MetadataScanner(metadata=module_info["metadata"])

            def init():
                metadata_scanner.scan()
                module: Module = module_info["module"]
                module.build(module_map)

            ExceptionsZone.run(init)

    def _build_module_map(
        self,
        module_cls: ModuleMetadata | EyrieModule,
        module_map: dict[str, dict[str, type | Module]] | None = None,
    ):
        if module_map is None:
            module_map = {}

        is_global = getattr(module_cls, MetaData.GLOBAL_MODULE, False)
        app_module = Module(_name=module_cls.__name__, _global=is_global)
        if app_module._id not in module_map:
            setattr(module_cls, "id", app_module._id)
            module_map[app_module._id] = {
                "metadata": module_cls,
                "module": app_module,
            }
            if issubclass(module_cls, EyrieModule) or hasattr(module_cls, "configure"):
                middleware_builder = MiddlewareBuilder()
                module_cls().configure(consumer=middleware_builder)
                module_map[app_module._id]["middlewares"] = middleware_builder.build()

            for import_cls in getattr(module_cls, "imports", []):
                self._build_module_map(import_cls, module_map)

        return module_map


EyrieFactory = EyrieFactoryStatic()
"""Use EyrieFactory to create an application instance.

### Specifying an entry module
Pass the required `root module` for the application via the module parameter.
By convention, it is usually called `ApplicationModule`. Starting with this
module, Nest assembles the dependency graph and begins the process of
Dependency Injection and instantiates the classes needed to launch your
application.
"""
