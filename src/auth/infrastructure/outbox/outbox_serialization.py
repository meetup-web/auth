import dataclasses
import json
from datetime import datetime
from typing import Any
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: object) -> Any:
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return None


class CustomJSONDecoder(json.JSONDecoder):
    def object_hook(self, obj: dict[str, Any]) -> dict[str, Any]:
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    obj[key] = UUID(value)
                    continue
                except ValueError:
                    pass

                try:
                    obj[key] = datetime.fromisoformat(value)
                    continue
                except ValueError:
                    pass
        return obj


def to_json(obj: object) -> str:
    return json.dumps(obj, cls=CustomJSONEncoder)


def from_json(json_string: str | bytes) -> Any:
    return json.loads(json_string, cls=CustomJSONDecoder)
