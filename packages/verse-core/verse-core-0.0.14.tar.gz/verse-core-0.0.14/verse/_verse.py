from abc import ABC, abstractmethod
from typing import Any

from ._provider import Provider


class Verse(ABC):
    @abstractmethod
    def provider(self, name: str, **kwargs: Any) -> Provider:
        pass
