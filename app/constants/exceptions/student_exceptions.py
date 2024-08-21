class StudentDocumentAlreadyExistsError(Exception):
    MESSAGE = "Student already exists in app"


class StudentNotFoundError(Exception):
    MESSAGE = "Student not found"