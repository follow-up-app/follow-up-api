import enum


class BillingEnum(enum.Enum):
    OPEN: str = 'PREVISTO'
    CONFIRMED: str = 'CONFIRMADO'
    DONE: str = 'FEITO'


class CategoryEnum(enum.Enum):
    PERSONAL: str = 'RESPONSÁVEL'
    PLAN: str = 'CONVÊNIO'
