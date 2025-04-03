import enum


class InvoiceSenderStatusEnum(enum.Enum):
    SENDER: str = 'ENVIADA'
    CANCELED: str = 'CANCELADA'

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
