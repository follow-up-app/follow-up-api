from app.core.invoice_requests import InvoiceRequests
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.billing_repository import BillingRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.health_plan_repository import HealthPlanRepository
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.repositories.address_contract_repository import AndressContractRepository
from app.schemas.invoice_schemas import InvoiceSchemaIn, InvoiceSchemaOut, InvoiceResponseApi
from app.schemas.company_schemas import CompanySchemaOut
from app.constants.exceptions.student_exceptions import StudentNotFoundError
from app.constants.exceptions.address_exceptions import AddressNotRegisterError
from app.constants.exceptions.responsible_contract_exceptions import ResponibleNotRegisterError
import datetime
from uuid import UUID
from typing import List
from types import SimpleNamespace


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
        value_total = 0
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        for billing_id in invoice_in.billings:
            billing = self.billing_repository.get_id(billing_id)
            value_total += billing.value

        if invoice_in.health_plan_id:
            health_plan = self.health_plan_repository.get_id(invoice_in.health_plan_id)

            taker = self.set_up_taker(health_plan.document, health_plan.social_name, health_plan.email)
            address = self.set_up_taker_address(health_plan)


        if invoice_in.responsible_id:
            responsible = self.responsible_repository.get_id(invoice_in.responsible_id)
            if not responsible:
                raise ValueError(ResponibleNotRegisterError.MESSAGE)
            address = self.address_contract_repository.get_contractor_id(student.contractor_id)
            if not address:
                raise ValueError(AddressNotRegisterError.MESSAGE)

            taker = self.set_up_taker(responsible.document, responsible.fullname, responsible.email)
            address = self.set_up_taker_address(address)

        provider = self.set_up_provider(company)
        service = self.set_up_service(
            company,
            billing.schedule.specialty.description,
            billing.schedule.specialty.code_nfes,
            value_total
            )

        payload = self.set_up_payload(provider, taker, address, service)

        ref = '000001'
        last_ref = self.invoice_repository.get_last_reference()
        if last_ref:
            ref = self.increment_number(last_ref.reference)

        sender = self.invoice_requests.sender_nfes(payload, ref)

        if sender.mensagem:
            raise ValueError(sender.mensagem)

        return self.save_invoice(sender, invoice_in.billings)

    def set_up_provider(self, company: CompanySchemaOut):
        provider = SimpleNamespace(
            cnpj = company.document,
            inscricao_municipal = company.municipal_registration,
            codigo_municipio = company.city_code
        )

        return provider

    def set_up_taker(self, document: str, social_name: str, email: str):
        taker = SimpleNamespace(
            cnpj = document,
            razao_social = social_name,
            email = email
        )

        return taker

    def set_up_taker_address(self, address):
        address = SimpleNamespace(
            logradouro = address.address,
            numero = address.number,
            complemento = address.complement,
            bairro = address.district,
            codigo_municipio = address.city_code,
            uf = address.state
        )

        return address

    def set_up_service(self, company: CompanySchemaOut, description: str, item_list_service: str, value: float):
        service = SimpleNamespace(
            aliquota = company.aliquot,
            discriminacao = description,
            iss_retido = False,
            item_lista_servico = item_list_service,
            valor_servicos = value
        )

        return service

    def set_up_payload(self, provider, taker, address, service):
        tomador = taker
        tomador.endereco = address

        payload = SimpleNamespace(
            data_emissao = datetime.datetime.now,
            prestador = provider,
            tomador = tomador,
            servico = service
        )

        return payload

    def by_reference(self, ref):
        return self.invoice_requests.reference_nfes(ref)

    def delete(self, ref):
        return self.invoice_requests.delete_nfes(ref)

    def sender_email(self, ref, email):
        return self.invoice_requests.sender_email(ref, email)

    def by_billing(self, billing_id: UUID):
        return self.invoice_repository.get_invoice_billing_all(billing_id)

    def increment_number(self, number_str: str) -> str:
        if not number_str.isdigit():
            raise ValueError("A entrada deve ser uma string numérica.")

        return str(int(number_str) + 1)

    def save_invoice(self, sender: InvoiceResponseApi, billings: List[UUID]) -> bool:
        invoice = self.invoice_repository.create_invoice_reference(sender)
        for billing_id in billings:
            self.invoice_repository.create_invoice_billing(invoice.id, billing_id)

        return True
