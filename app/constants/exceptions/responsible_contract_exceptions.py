class ResponibleDocumentAlreadyExistsError(Exception):
    MESSAGE = "Responible already exists in app"


class ResponibleNotFoundError(Exception):
    MESSAGE = "Responible not found"


class ResponibleNotRegisterError(Exception):
    MESSAGE = "O cliente não possui nenhum responsável cadastado. Faça o cadastro de um endereço em responsável > cliente > responsáveis"
