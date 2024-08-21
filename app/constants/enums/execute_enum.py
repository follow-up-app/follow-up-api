import enum


class ExecuteEnum(enum.Enum):
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'CONCLUÍDO'
