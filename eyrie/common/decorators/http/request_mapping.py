from types import FunctionType

from eyrie.common.constants import HTTPMethodType


def create_mapping_decorator(method: HTTPMethodType, path: str, **kwargs):
    def decorator(func: FunctionType):
        func.method = method
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator


def Get(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP GET requests to the
    specified path.
    """
    return create_mapping_decorator("GET", path, **kwargs)


def Post(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP POST requests to the
    specified path.
    """
    return create_mapping_decorator("POST", path, **kwargs)


def Delete(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP DELETE requests to the
    specified path.
    """
    return create_mapping_decorator("DELETE", path, **kwargs)


def Put(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP PUT requests to the
    specified path.
    """
    return create_mapping_decorator("PUT", path, **kwargs)


def Patch(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP PATCH requests to the
    specified path.
    """
    return create_mapping_decorator("PATCH", path, **kwargs)


def Options(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP OPTIONS requests to the
    specified path.
    """
    return create_mapping_decorator("OPTIONS", path, **kwargs)


def Head(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP HEAD requests to the
    specified path.
    """
    return create_mapping_decorator("HEAD", path, **kwargs)


def Trace(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP TRACE requests to the
    specified path.
    """
    return create_mapping_decorator("TRACE", path, **kwargs)


def Connect(path: str = "", **kwargs):
    """Route handler (method) Decorator. Routes HTTP CONNECT requests to the
    specified path.
    """
    return create_mapping_decorator("CONNECT", path, **kwargs)
