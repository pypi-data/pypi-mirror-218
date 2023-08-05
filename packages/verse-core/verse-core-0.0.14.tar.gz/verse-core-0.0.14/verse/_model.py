import json
from datetime import datetime
from typing import Any


class _CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class Model:
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, cls=_CustomJSONEncoder)

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
