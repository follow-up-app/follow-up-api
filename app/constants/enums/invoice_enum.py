import enum


class InvoiceEnum(enum.Enum):
    NOT_FOUND: str = 'NÃO ENCONTADO'
    CANCELED: str = 'CANCELADA'
    NOT_AUTHORIZED: str = 'NÃO AUTORIZADA'
    INVALID_REQUEST: str = 'REQUSIÇÃO INVÁLIDA'
    COMPANY_NOT_QUALIFIED: str = 'EMPRESA NÃO HABILITADA'
    CERTIFICATE_EXPIRED: str = 'CERTIFICADO EXPIRADO'
    AUTHORIZED: str = 'AUTORIZADA'
    IN_PROCESS: str = 'EM PROCESSAMENTO'


class ExternalApiResponse(enum.Enum):
    NOT_FOUND: str = 'nao_encontrado'
    CANCELED: str = 'nfe_cancelada'
    NOT_AUTHORIZED: str = 'nfe_nao_autorizada'
    INVALID_REQUEST: str = 'requisicao_invalida'
    COMPANY_NOT_QUALIFIED: str = 'empresa_nao_habilitada'
    CERTIFICATE_EXPIRED: str = 'certificado_vencido'
    AUTHORIZED: str = 'nfe_autorizada'
    IN_PROCESS: str = 'em_processamento'
    PROCESS_AUTHORIZED: str = 'processando_autorizacao'
