import enum


class PaymentEnum(enum.Enum):
    OPEN: str = 'PREVISTO'
    SCHEDULED: str = 'CONFIRMADO'
    DONE: str = 'FEITO'
