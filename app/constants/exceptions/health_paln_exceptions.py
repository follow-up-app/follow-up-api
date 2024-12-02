class HealthPlanNotFoundError(Exception):
    MESSAGE = "Health plan not found"
    
class HealthPlanExistsError(Exception):
    MESSAGE = "Já existe um plano cadastrado com esse documento"