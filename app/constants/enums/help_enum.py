import enum


class HelpEnum(enum.Enum):
    DEPENDENT: str = 'DEPENDENTE'
    INDEPENDENT: str = 'INDEPENDENTE'
    POSITIONAL: str = 'POSICIONAL'
    GESTURE: str = 'GESTUAL'
    VERBAL: str = 'VERBAL'
    PHYSICAL: str = 'FÍSICA'
    VISUAL: str = 'VISUAL'
    NOT_EXECUTED: str = 'NÃO EXECUTADO'
