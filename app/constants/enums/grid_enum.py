import enum


class GridEnum(enum.Enum):
    SCHEDULED: str = 'AGENDADO'
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'CONCLUÍDO'