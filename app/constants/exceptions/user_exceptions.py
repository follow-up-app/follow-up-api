class UserDocumentAlreadyExistsError(Exception):
    MESSAGE = "Document already exists in app"


class UserEmailNotFoundError(Exception):
    MESSAGE = "Email not found"


class UserNotFoundError(Exception):
    MESSAGE = "User not found"


class UserEmailDocumentAlreadyExistsError(Exception):
    MESSAGE = "Email already exists in app"