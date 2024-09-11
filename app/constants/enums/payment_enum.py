import enum


class PaymentEnum(enum.Enum):
    OPEN: str = 'EM ABERTO'
    SCHEDULED: str = 'AGENDADO'
    DONE: str = 'FEITO'    