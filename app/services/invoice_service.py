from app.core.invoice_requests import InvoiceRequests
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.billing_repository import BillingRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.health_plan_repository import HealthPlanRepository
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.repositories.address_contract_repository import AndressContractRepository
from app.schemas.invoice_schemas import InvoiceSchemaIn, InvoiceSchemaOut
from app.schemas.company_schemas import CompanySchemaOut
from app.constants.exceptions.student_exceptions import StudentNotFoundError
from app.constants.exceptions.address_exceptions import AddressNotRegisterError
from app.constants.exceptions.responsible_contract_exceptions import ResponibleNotRegisterError
import datetime
from uuid import UUID


class InvoiceService:
    def __init__(self,
                 company_repositoy: CompanyRepository,
                 student_repository: StudentRepository,
                 billing_repository: BillingRepository,
                 invoice_repository: InvoiceRepository,
                 health_plan_repository: HealthPlanRepository,
                 responsible_repository: ResponsibleContractRepository,
                 address_contract_repository: AndressContractRepository,
                 invoice_requests: InvoiceRequests):
        self.company_repositoy = company_repositoy
        self.student_repository = student_repository
        self.billing_repository = billing_repository
        self.invoice_repository = invoice_repository
        self.health_plan_repository = health_plan_repository
        self.responsible_repository = responsible_repository
        self.address_contract_repository = address_contract_repository
        self.invoice_requests = invoice_requests

    def sender(self, invoice_in: InvoiceSchemaIn) -> InvoiceSchemaOut:
        company = self.company_repositoy.company_by_user_logged()
        student = self.student_repository.get_id(invoice_in.student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        for billing_id in invoice_in.billings:
            billing = self.billing_repository.get_id(billing_id)
            value_total += billing.value

        if invoice_in.health_plan_id:
            health_plan = self.health_plan_repository.get_id(
                invoice_in.health_plan_id)
            taker = self.set_up_taker(
                health_plan.document, health_plan.social_name, health_plan.email)
            address = self.set_up_taker_address(health_plan)

        if invoice_in.responsible_id:
            responsible = self.responsible_repository.get_id(
                invoice_in.responsible_id)
            if not responsible:
                raise ValueError(ResponibleNotRegisterError.MESSAGE)
            address = self.address_contract_repository.get_contractor_id(
                student.contractor_id)
            if not address:
                raise ValueError(AddressNotRegisterError.MESSAGE)

            taker = self.set_up_taker(
                responsible.document, responsible.fullname, responsible.email)
            address = self.set_up_taker_address(address)

        provider = self.set_up_provider(company)
        service = self.set_up_service(
            company, billing.schedule.specialty.description, billing.schedule.specialty.code_nfes, value_total)

        payload = self.set_up_payload(provider, taker, address, service)

        # temporary
        ref = '1212'

        sender = self.invoice_requests.sender_nfes(payload, ref)

        if sender.mensagem:
            raise ValueError(sender.mensagem)

        return self.invoice_repository.create_invoice_reference(ref)

    def set_up_provider(self, company: CompanySchemaOut):
        provider = []
        provider.cnpj = company.document
        provider.inscricao_municipal = company.municipal_registration
        provider.codigo_municipio = company.city_code

        return provider

    def set_up_taker(self, document: str, social_name: str, email: str):
        taker = []
        taker.cnpj = document
        taker.razao_social = social_name
        taker.email = email

        return taker

    def set_up_taker_address(self, taker):
        address = []
        address.logradouro = taker.address
        address.numero = taker.number
        address.complemento = taker.complement
        address.bairro = taker.district
        address.codigo_municipio = taker.city_code
        address.uf = taker.state

        return address

    def set_up_service(self, company: CompanySchemaOut, description: str, item_list_service: str, value: float):
        service = []
        service.aliquota = company.aliquot
        service.discriminacao = description
        service.iss_retido = False
        service.item_lista_servico = item_list_service
        service.valor_servicos = value

        return service

    def set_up_payload(self, provider, taker, address, service):
        payload = []
        payload.data_emissao = datetime.datetime.now
        payload.prestador = provider
        payload.tomador = taker
        payload.tomador.endereco = address
        payload.servico = service

        return payload

    def by_reference(self, ref):
        return self.invoice_requests.reference_nfes(ref)

    def delete(self, ref):
        return self.invoice_requests.delete_nfes(ref)

    def sender_email(self, ref, email):
        return self.invoice_requests.sender_email(ref, email)

    def by_billing(self, billing_id: UUID):
        return self.invoice_repository.get_invoice_billing_all(billing_id)
