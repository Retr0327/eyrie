from eyrie.common.constants import Watermark


def Injectable():
    """Decorator that marks a class as a [provider](https://python-dependency-injector.ets-labs.org/providers/index.html).
    Providers can be injected into other classes via constructor parameter injection.
    """

    def wrapper(cls: type) -> type:
        setattr(cls, Watermark.INJECTABLE, True)
        return cls

    return wrapper
