import enum

class PartenalEnum(enum.Enum):
    FATHER: str = 'PAI'
    MOTHER: str = 'MÃE'
    UNCLES: str = 'TIOS'
    GRANDPARENTS: str = 'AVÓS'
    OTHERS: str = 'OUTROS'