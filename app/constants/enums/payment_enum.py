import enum


class PaymentEnum(enum.Enum):
    OPEN: str = 'PREVISTO'
    SCHEDULED: str = 'AGENDADO'
    DONE: str = 'FEITO'
