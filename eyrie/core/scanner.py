from dataclasses import dataclass
import inspect

from .errors import UndefinedDependencyException
from .injector import Module


@dataclass(slots=True)
class DependenciesScanner:
    modules: list[Module]
    providers: dict

    def _scan_dependencies(self, cls_info: dict, module: Module):
        cls, host_id = cls_info["token"], cls_info["host"]
        try:
            deps = inspect.signature(cls).parameters
        except Exception:
            deps = {}

        for dep in deps.values():
            should_skip = (
                dep.annotation is inspect._empty or dep.default is inspect._empty
            )
            if should_skip:
                continue

            dep_info = self.providers.get(dep.annotation)
            if dep_info is None:
                raise UndefinedDependencyException(dep.annotation, module._name, cls)

            dep_host_id = dep_info["host"]
            if dep_host_id == host_id:
                continue

            dep_module = next(i for i in self.modules if i._id == dep_host_id)
            if not dep_module._global and dep_module not in module._imports:
                raise UndefinedDependencyException(dep.annotation, module._name, cls)

    def scan(self):
        for module in self.modules:
            for provider_info in module._providers.values():
                self._scan_dependencies(provider_info, module)

            for guard_info in module._guards.values():
                self._scan_dependencies(guard_info, module)

            for middleware_info in module._middlewares.values():
                self._scan_dependencies(middleware_info, module)
