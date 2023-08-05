from .exceptions import (
    ExistsError,
    NotFoundError,
    NotSupportedError,
    ProviderError,
)

__all__ = ["client_api"]


def client_api(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (NotFoundError, ExistsError, NotSupportedError):
            raise
        except Exception as e:
            raise ProviderError from e

    return wrapper
