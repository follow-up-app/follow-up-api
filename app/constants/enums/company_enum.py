import enum


class CompanyEnum(enum.Enum):
    ACTIVE: str = "ATIVA"
    IN_ANALYSIS: str = "EM ANALISE"
    BLOCKED: str = "BLOQUEADA"
    INACTIVE: str = "INATIVA"
