from eyrie.common.constants import MetaData


def Global():
    """Decorator that makes a module global-scoped.

    Once imported into any module, a global-scoped module will be visible
    in all modules. Thereafter, modules that wish to inject a service exported
    from a global module do not need to import the provider module.
    """

    def wrapper(cls: type):
        setattr(cls, MetaData.GLOBAL_MODULE, True)
        return cls

    return wrapper
