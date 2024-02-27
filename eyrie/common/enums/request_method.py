from enum import StrEnum


class RequestMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    ALL = "ALL"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    SEARCH = "SEARCH"
