import requests
from config import get_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiRequests:
    def __init__(self):
        self._settings = get_settings()

    def banks(self):
        url = self._settings.BANKS_URL
        try:
            response = requests.get(url)
            return response.json()

        except Exception as e:
            logger.error(f"Error in request bank list: {e}")
            raise ValueError('Error in request')

    def cep(self, cep: str):
        url = self._settings.CEP_URL + cep + '/json'

        try:
            response = requests.get(url)
            return response.json()

        except Exception as e:
            logger.error(f"Error in request cep: {e}")
            raise ValueError('Error in request')
