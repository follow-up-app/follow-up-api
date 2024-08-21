class ProcedureNotFoundError(Exception):
    MESSAGE = "Procedure not found"
    
class ProcedureExecutionError(Exception):
    MESSAGE = "Já existe execução deste objetivo. Para excluir, entre em contado com suporte do sistema!"