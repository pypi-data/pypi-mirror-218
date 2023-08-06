class CqlPyError(Exception):
    ...


class CqlParseError(CqlPyError, ValueError):
    ...


class ValuesetProviderError(CqlPyError):
    ...
