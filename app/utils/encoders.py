import json
from uuid import UUID
from app.constants.enums.permission_enum import PermissionEnum


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        if isinstance(obj, PermissionEnum):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
