class InstructorNotFoundError(Exception):
    MESSAGE = "Instructor not found"
    
class InstructorUserCreateError(Exception):
    MESSAGE = "Email or document already exists in app"