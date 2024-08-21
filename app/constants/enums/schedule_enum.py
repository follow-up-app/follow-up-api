import enum


class ScheduleEnum(enum.Enum):
    SCHEDULED: str = 'AGENDADO'
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DID_NOT_ATTEND: str = 'NÃO COMPARECEU'
    DONE: str = 'CONCLUÍDO'