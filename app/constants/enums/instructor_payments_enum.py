import enum


class TypePaymentEnum(enum.Enum):
    PIX: str = 'PIX'
    TRANSFER: str = 'TED'


class ModePaymentEnum(enum.Enum):
    MOUNTH: str = 'MENSAL'
    WEEK: str = 'SEMANAL'
    DAY: str = 'DIARIA'
    HOUR: str = 'HORA'
    COMISSION: str = 'COMISSÃO'
