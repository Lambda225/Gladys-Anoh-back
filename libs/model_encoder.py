from typing import Any
from flask import json
class ModelEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return super(ModelEncoder, self).default(o)
