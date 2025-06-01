import enum


class BillingEnum(enum.Enum):
    OPEN: str = 'PREVISTO'
    GENERATE_INVOICE: str = 'GERADO NFSe'
    CONFIRMED: str = 'CONFIRMADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'FEITO'


class CategoryEnum(enum.Enum):
    PERSONAL: str = 'RESPONSÁVEL'
    PLAN: str = 'CONVÊNIO'
