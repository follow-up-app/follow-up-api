from app.core.invoice_requests import InvoiceRequests
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.billing_repository import BillingRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.health_plan_repository import HealthPlanRepository
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.repositories.address_contract_repository import AndressContractRepository
from app.schemas.invoice_schemas import InvoiceSchemaIn, InvoiceSenderApi, InvoiceResponseApi
from app.schemas.company_schemas import CompanySchemaOut
from app.schemas.specialty_schemas import SpecialtySchemaOut
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.student_schemas import StudentSchemaOut
from app.constants.exceptions.student_exceptions import StudentNotFoundError
from app.constants.exceptions.address_exceptions import AddressNotRegisterError
from app.constants.exceptions.responsible_contract_exceptions import ResponibleNotRegisterError
import datetime
from uuid import UUID
from typing import List
from app.constants.enums.billing_enum import BillingEnum
from app.core.utils import Util
import re

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

    def sender(self, invoice_in: InvoiceSchemaIn) -> bool:
        self.validate_billings_invoice(invoice_in.billings)

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
        description = self.set_up_description(billing.schedule.specialty, billing.schedule.instructor, student, value_total)
        service = self.set_up_service(
            company,
            description,
            billing.schedule.specialty.code_nfes,
            value_total
            )

        payload = self.set_up_payload(provider, taker, address, service)
        ref = self.generate_ref()
        # sender = self.invoice_requests.sender_nfes(payload, ref)

        # self.save_invoice(sender, invoice_in.billings)
        self.update_billing(invoice_in.billings)

        return ref

    def set_up_provider(self, company: CompanySchemaOut):
        provider = {
            'cnpj': re.sub(r'\D', '', company.document),
            'inscricao_municipal': company.municipal_registration,
            'codigo_municipio': Util.search_cod_municipalities(company.city, company.state)
        }

        return provider

    def set_up_taker(self, document: str, social_name: str, email: str):
        taker = {
            'cnpj': re.sub(r'\D', '', document),
            'razao_social': social_name,
            'email': email
        }

        return taker

    def set_up_taker_address(self, address):
        address = {
            'logradouro': address.address,
            'numero': address.number,
            'complemento': address.complement,
            'bairro': address.district,
            'codigo_municipio': Util.search_cod_municipalities(address.city, address.state),
            'uf': address.state,
            'cep': re.sub(r'\D', '', address.zip_code),
        }

        return address

    def set_up_description(self, specialty: SpecialtySchemaOut, instructor: InstructorSchemaOut, student: StudentSchemaOut, value_total: float) -> str:
        return f"{specialty.description} COM PROFISSIONAL {instructor.fullname} - CRP: {instructor.crp} PARA O BENEFICIÁRIO {student.fullname} - NO VALOR DE {int(specialty.value_hour)},00/HORA. TOTAL DE SESSÕES: {int(value_total)},00."

    def set_up_service(self, company: CompanySchemaOut, description: str, item_list_service: str, value: float):
        service = {
            'aliquota': company.aliquot,
            'discriminacao': description,
            'iss_retido': False,
            'item_lista_servico': item_list_service,
            'situacao_tributaria': 0,
            'valor_servicos': int(value)
        }

        return service

    def set_up_payload(self, provider, taker, address, service):
        tomador = taker.copy()
        tomador['endereco'] = address

        payload = {
            'data_emissao': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'prestador': provider,
            'tomador': tomador,
            'servico': service
        }

        return payload

    def by_reference(self, ref):
        return self.invoice_requests.reference_nfes(ref)

    def delete(self, ref):
        return self.invoice_requests.delete_nfes(ref)

    def sender_email(self, ref, email):
        return self.invoice_requests.sender_email(ref, email)

    def by_billing(self, billing_id: UUID):
        invoice_billing =  self.invoice_repository.get_invoice_for_billing(billing_id)
        if not invoice_billing:
            raise ValueError("Não existe NFSe para esta cobrança.")

        return self.invoice_requests.reference_nfes(invoice_billing.invoice.reference)

    def generate_ref(self) -> str:
        ref = '000001'
        last_ref = self.invoice_repository.get_last_reference()
        if last_ref:
            length = len(ref)
            incremented = int(ref) + 1

            ref = str(incremented).zfill(length)

        return ref

    def validate_billings_invoice(self, billings: List[UUID]) -> bool:
        for billing_id in billings:
            billing = self.invoice_repository.get_invoice_for_billing(billing_id)
            if billing:
                raise ValueError("Já existe NFSe para alguma das cobranças selecionadas.")

        return True

    def save_invoice(self, sender: InvoiceSenderApi, billings: List[UUID]) -> bool:
        invoice = self.invoice_repository.create_invoice_reference(sender)
        for billing_id in billings:
            self.invoice_repository.create_invoice_billing(invoice.id, billing_id)

        return True

    def update_billing(self, billings: List[UUID]) -> bool:
        for bill in billings:
            billing = self.billing_repository.get_id(bill)

            self.billing_repository.update_status(billing, BillingEnum.GENERATE_INVOICE)

        return True