import enum


class PaymentEnum(enum.Enum):
    OPEN: str = "PREVISTO"
    CONFIRMED: str = 'CONFIRMADO'
    CANCELED: str = "CANCELADO"
    GENERATE_ORDER: str = "FEITO"


class OrderPaymentEnum(enum.Enum):
    SCHEDULED: str = "GERADO"
    CANCELED: str = "CANCELADO"
    DONE: str = "FEITO"
