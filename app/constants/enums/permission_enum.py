import enum


class PermissionEnum(enum.Enum):
    ADMIN: str = 'ADMIN'
    INSTRUCTOR: str = 'INSTRUCTOR'
    PARENTS: str = 'PARENTS'
