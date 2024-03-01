from dataclasses import dataclass
import inspect

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.routing import (
    Route,
    WebSocketRoute,
)


@dataclass(slots=True)
class RouterProxy:
    controller: type
    router: APIRouter

    def _get_routes(self):
        methods = inspect.getmembers(self.controller, inspect.isfunction)
        method_set = {method for _, method in methods}
        routes = []
        for route in self.router.routes:
            is_valid = isinstance(route, (Route, WebSocketRoute))
            if is_valid and route.endpoint in method_set:
                routes.append(route)
        return routes

    def _update_signature_by_controller(self, route: Route | WebSocketRoute):
        prev_signatures = inspect.signature(route.endpoint)
        prev_params = list(prev_signatures.parameters.values())
        prev_self, *prev_rest_params = prev_params
        new_self = prev_self.replace(default=Depends(self.controller))
        new_params = [new_self]
        for param in prev_rest_params:
            new_params.append(param.replace(kind=inspect.Parameter.KEYWORD_ONLY))

        new_signature = prev_signatures.replace(parameters=new_params)
        setattr(route.endpoint, "__signature__", new_signature)

    def create(self):
        controller_router = APIRouter()
        controller_routes = self._get_routes()
        for route in controller_routes:
            self.router.routes.remove(route)
            self._update_signature_by_controller(route)
            controller_router.routes.append(route)

        self.router.include_router(controller_router)
        return self.controller
