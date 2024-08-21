class CompanyDocumentAlreadyExistsError(Exception):
    MESSAGE = "Document already exists in app"
    
class CompanyNotFoundError(Exception):
    MESSAGE = "Company not found"