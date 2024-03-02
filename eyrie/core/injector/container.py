import inspect
from types import (
    FunctionType,
    LambdaType,
)

from dependency_injector import providers as _providers
from dependency_injector.containers import DynamicContainer

from eyrie.core.inspector import GraphInspector
from eyrie.core.utils import get_provider_token


class EyrieContainer(DynamicContainer):
    def __init__(self) -> None:
        super().__init__()
        self.__modules = set()
        self._di_graph = GraphInspector()

    def add_provider(self, provider: dict):
        provider_cls, provider_name = provider["token"], provider["name"]
        if hasattr(self, provider_name):
            return

        provide = getattr(_providers, provider["scope"].capitalize())
        self.__modules.add(provider_cls.__module__)
        cls_params = inspect.signature(provider_cls).parameters
        if not cls_params:
            return setattr(self, provider_name, provide(provider_cls))

        deps = provider.get("custom_deps", {})
        for key, dep in cls_params.items():
            if key not in deps and dep.default is not inspect._empty:
                dep_token = get_provider_token(dep.annotation)
                dep_provider = getattr(self, dep_token, None)
                if dep_provider is not None:
                    deps[key] = dep_provider

        return setattr(self, provider_name, provide(provider_cls, **deps))

    def get_resolved_providers(self, providers: dict):
        for provider in providers.keys():
            self._di_graph.add_provider(provider)
            deps = inspect.signature(provider).parameters
            for dep in deps.values():
                if (
                    isinstance(dep.annotation, (type, FunctionType, LambdaType))
                    and dep.annotation is not inspect._empty
                ):
                    self._di_graph.add_dep(provider, dep.annotation)

        return self._di_graph.resolve_providers()

    def wire(self, modules: set = set()):
        self.__modules.update(modules)
        return super().wire(modules=self.__modules)
