import enum


class CompanyEnum(enum.Enum):
    ACTIVE: str = 'ATIVO'
    IN_ANALYSIS: str = 'EM ANALISE'
    BLOCKED: str = 'BLOQUEADO'
    DESACATIVE: str = 'DESATIVADO'
