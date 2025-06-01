import requests
from config import get_settings
import logging
from requests.auth import HTTPBasicAuth
from app.schemas.company_schemas import CompanySchemaOut
from app.schemas.invoice_schemas import InvoiceResponseApi, InvoiceSenderApi

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

    def sender_nfes(self, data, ref) -> InvoiceSenderApi:
        try:
            response = requests.post(
                url=f"{self.url}/v2/nfse?ref={ref}",
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw),
                json=data
            )
            if response.status_code != 201:
                logger.error(f"Error in call api NFEs: {response.status_code} - {response.text} - ref: {ref} - payload: {data}")
                raise ValueError(f"HTTP Error: {response.status_code}")

            return response.json()

        except Exception as e:
            logger.error(f"Error in sender nfes: {e}")
            raise ValueError('Error in sender nfes')


    def reference_nfes(self, ref) -> InvoiceResponseApi:
        try:
            # response = requests.get(
            #     url=f"{self.url}/v2/nfse/REFERENCIA/{ref}",
            #     headers=self.headers,
            #     auth=HTTPBasicAuth(self.username, self.passw))

            # if response.status_code != 200:
            #     logger.error(f"Error in call api NFEs: {response.status_code} - {response.text} - ref: {ref}")
            #     raise ValueError(f"HTTP Error: {response.status_code}")

            # return response.json()
            response = InvoiceResponseApi(
                cnpj_prestador='07504505000132',
                ref='000001',
                numero_rps='224',
                serie_rps='1',
                status='autorizado',

                numero='233',
                codigo_verificacao='DU1M-M2Y',
                data_emissao='2019-05-27T00:00:00-03:00',
                url='https://200.189.192.82/PilotoNota_Portal/Default.aspx?doc=07504505000132&num=233&cod=DUMMY',
                caminho_xml_nota_fiscal='/arquivos/07504505000132_12345/202401/XMLsNFSe/075045050001324106902-004949940-433-DUMMY-nfse.xml',
                caminho_xml_cancelamento='/arquivos/07504505000132_12345/202401/XMLsNFSe/075045050001324106902-004949940-433-DUMMY-nfse.xml',
        )
            response.caminho_xml_nota_fiscal =f"{self.url}/{response.caminho_xml_nota_fiscal}"
            if response.caminho_xml_cancelamento:
                response.caminho_xml_cancelamento =f"{self.url}/{response.caminho_xml_cancelamento}"


            return response

        except Exception as e:
            logger.error(f"Error in query nfes: {e}")
            raise ValueError('Error in query nfes')

    def delete_nfes(self, ref):
        try:
            response = requests.delete(
                url=f"{self.url}/v2/nfse/REFERENCIA/{ref}",
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw))

            if response.status_code != 200:
                logger.error(f"Error in call api NFEs: {response.status_code} - {response.text} - ref: {ref}")
                raise ValueError(f"HTTP Error: {response.status_code}")

            return response.json()

        except Exception as e:
            logger.error(f"Error in delete nfes: {e}")
            raise ValueError('Error in delete nfe')

    def sender_email(self, ref, email):
        try:
            response = requests.post(
                url=f"{self.url}/v2/nfse/ref/{ref}/{email}",
                headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.passw))

            if response.status_code != 200:
                logger.error(f"Error in call api NFEs: {response.status_code} - {response.text} - ref: {ref} - email: {email}")
                raise ValueError(f"HTTP Error: {response.status_code}")

            return response.json()

        except Exception as e:
            logger.error(f"Error in sender mail nfes: {e}")
            raise ValueError('Error in sender mail nfes')
