from typing import Any, Dict, Optional

from ._provider import Provider
from ._types import Action


class Resource:
    provider: Provider

    def __init__(self, provider: Optional[Provider] = None, **kwargs):
        if provider is not None:
            self.provider = provider

    def set_provider(self, provider: Provider) -> None:
        self.provider = provider

    def execute(
        self,
        action: Action | str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return self.provider.execute(action=action, params=params, **kwargs)

    async def aexecute(
        self,
        action: Action | str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return await self.provider.aexecute(
            action=action, params=params, **kwargs
        )
