from __future__ import annotations

from dataclasses import dataclass
from types import FunctionType
from typing import TYPE_CHECKING

from eyrie.common.constants import (
    MetaData,
    Watermark,
)

from .errors.exceptions import (
    InvalidClassModuleException,
    InvalidControllerException,
    InvalidModuleTypeException,
    RuntimeException,
    UnknownExportException,
)

if TYPE_CHECKING:
    from eyrie.common.interfaces import (
        ModuleMetadata,
        ProviderConfig,
    )


@dataclass(slots=True)
class MetadataScanner:
    metadata: ModuleMetadata

    def is_injectable(self, provider: type | FunctionType):
        return getattr(provider, Watermark.INJECTABLE, False)

    def is_controller(self, controller: type | FunctionType):
        return getattr(controller, Watermark.CONTROLLER, False)

    def scan_controllers(self, controllers: list[type | FunctionType]):
        for controller in controllers:
            if not self.is_controller(controller):
                raise InvalidControllerException(controller=controller)

    def scan_exports(self, exports: list[type | FunctionType | ProviderConfig]):
        for export in exports:
            if export not in self.metadata.providers:
                raise UnknownExportException(provider=export, module=self.metadata)

    def scan_imports(self, modules: list[type | FunctionType]):
        for module in modules:
            if self.is_controller(module) or self.is_injectable(module):
                raise InvalidClassModuleException(provider=module, module=self.metadata)

            global_marker = getattr(module, MetaData.GLOBAL_MODULE, None)
            if not isinstance(module, type) or global_marker is None:
                raise InvalidModuleTypeException(module=module)

    def scan_providers(self, providers: list[type | FunctionType | ProviderConfig]):
        for provider in providers:
            if isinstance(provider, (type, FunctionType)):
                continue

            provide_cls, inject = provider.get("provide"), provider.get("inject", [])
            if not inject and isinstance(provide_cls, str):
                raise RuntimeException(
                    f"Provide {provide_cls} must be a class or a function if "
                    "inject is not provided"
                )
            if len(inject) > 2:
                raise RuntimeException("Inject must be a list of 2 elements")
            if inject:
                if not isinstance(inject[0], (type | FunctionType)):
                    raise RuntimeException(
                        "The first element of inject must be a class or a function"
                    )
                if isinstance(provide_cls, str) and isinstance(inject[0], str):
                    raise RuntimeException(
                        "One of the Provide and inject must be a class or a function"
                    )
                if len(inject) == 2 and not isinstance(inject[1], dict):
                    raise RuntimeException(
                        "The second element of inject must be a dictionary"
                    )

    def scan(self):
        factories = {
            "imports": self.scan_imports,
            "controllers": self.scan_controllers,
            "providers": self.scan_providers,
            "exports": self.scan_exports,
        }
        for field, callback in factories.items():
            value = getattr(self.metadata, field, [])
            callback(value)
