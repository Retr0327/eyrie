from types import FunctionType

from eyrie.core.errors.messages import INVALID_DECORATOR_ITEM_MESSAGE

from .runtime import RuntimeException


class InvalidDecoratorItemException(RuntimeException):
    def __init__(self, target: type | FunctionType, item: str, decorator: str) -> None:
        msg = INVALID_DECORATOR_ITEM_MESSAGE(target, item, decorator)
        super().__init__(msg=msg)
