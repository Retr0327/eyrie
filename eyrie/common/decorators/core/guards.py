from collections.abc import Sequence
from types import FunctionType

from eyrie.common.constants import Watermark
from eyrie.common.interfaces.features import CanActivate
from eyrie.core.errors import InvalidDecoratorItemException


def UseGuards(*guards: Sequence[type | FunctionType]):
    """Decorator that binds guards to the scope of the controller or method,
    depending on its context. When `@UseGuards` is used at the controller level,
    the guard will be applied to every handler (method) in the controller.
    When `@UseGuards` is used at the individual handler level, the guard will
    apply only to that specific method.

    Args:
        guards (Sequence[type | FunctionType]): a single guard instance or
        class, or a list of guard instances or classes.
    """

    def wrapper(obj: type | FunctionType):
        for guard in guards:
            if isinstance(obj, type) and not issubclass(guard, CanActivate):
                raise InvalidDecoratorItemException(obj, "guards", "@UseGuards")

        setattr(obj, Watermark.GUARDS, guards)
        return obj

    return wrapper
