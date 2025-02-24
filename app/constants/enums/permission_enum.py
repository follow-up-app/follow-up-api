import enum


class PermissionEnum(enum.Enum):
    OWER: str = 'OWER'
    ADMIN: str = 'ADMIN'
    INSTRUCTOR: str = 'INSTRUCTOR'
    PARENTS: str = 'PARENTS'
