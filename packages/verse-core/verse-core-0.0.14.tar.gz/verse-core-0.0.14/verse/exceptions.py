__all__ = [
    "ExistsError",
    "NotFoundError",
    "NotSupportedError",
    "ProviderError",
]


class NotFoundError(Exception):
    pass


class ExistsError(Exception):
    pass


class NotSupportedError(Exception):
    pass


class ProviderError(Exception):
    pass
