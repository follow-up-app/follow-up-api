import requests
from config import get_settings
import logging
from requests.auth import HTTPBasicAuth
from app.schemas.company_schemas import CompanySchemaOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceRequests:
    def __init__(self, company: CompanySchemaOut):
        self._settings = get_settings()
        self.url = self._settings.NFSE_HOST
        self.username = company.api_nfes_token
        self.passw = ''
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def sender_nfes(self, data, ref):
        try:
            response = requests.post(
                url=self.url & '/v2/nfse?ref=' & ref,
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw),
                json=data)
            return response.json()

        except Exception as e:
            logger.error(f"Error in sender nfes: {e}")
            raise ValueError('Error in sender nfes')

    def reference_nfes(self, ref):
        try:
            response = requests.get(
                url=self.url & '/v2/nfse/REFERENCIA/' & ref,
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw))
            return response.json()

        except Exception as e:
            logger.error(f"Error in query nfes: {e}")
            raise ValueError('Error in query nfes')

    def delete_nfes(self, ref):
        try:
            response = requests.delete(
                url=self.url & '/v2/nfse/REFERENCIA/' & ref,
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw))
            return response.json()

        except Exception as e:
            logger.error(f"Error in delete nfes: {e}")
            raise ValueError('Error in delete nfe')

    def sender_email(self, ref, email):
        try:
            response = requests.post(
                url=self.url & '/v2/nfse/ref/' & ref & '/'& email,
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw))
            return response.json()

        except Exception as e:
            logger.error(f"Error in sender mail nfes: {e}")
            raise ValueError('Error in sender mail nfes')
