from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ._helpers import AsyncHelper
from ._types import Action


class Provider(ABC):
    def execute(
        self,
        action: Action | str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        if isinstance(action, Action):
            return self._execute(action=action, **kwargs)

    async def aexecute(
        self,
        action: Action | str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        if isinstance(action, Action):
            return self._aexecute(action=action, **kwargs)

    @abstractmethod
    def _execute(self, action: Action, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _aexecute(self, action: Action, **kwargs: Any) -> Any:
        return await AsyncHelper.to_async(
            func=self.execute, action=action, **kwargs
        )
