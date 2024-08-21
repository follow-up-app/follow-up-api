class ResponibleDocumentAlreadyExistsError(Exception):
    MESSAGE = "Responible already exists in app"


class ResponibleNotFoundError(Exception):
    MESSAGE = "Responible not found"