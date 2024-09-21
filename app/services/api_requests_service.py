from app.core.api_requests import ApiRequests


class ApiRequestsService:
    def __init__(self):
        self.api_requests = ApiRequests()

    def banks(self):
        return self.api_requests.banks()

    def cep(self, cep: str):
        return self.api_requests.cep(cep)
