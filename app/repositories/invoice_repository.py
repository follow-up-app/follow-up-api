from sqlalchemy.orm import Session
from db.models import Invoice, InvoiceLog, InvoiceBilling, User
from app.constants.enums.invoice_enum import InvoiceSenderStatusEnum
from app.schemas.invoice_schemas import InvoiceLogSchemaOut, InvoiceSchemaOut, InvoiceBillingSchemaOut, InvoiceSchemaIn, InvoiceSenderApi
from uuid import UUID
from typing import List


class InvoiceRepository:
    def __init__(self, session: Session, current_user: User) -> InvoiceSchemaOut:
        self.session = session
        self.current_user = current_user

    def create_invoice_reference(self, response_api: InvoiceSenderApi):
        invoice = Invoice(
            company_id=self.current_user.company_id,
            reference=response_api.ref,
            api_status=response_api.status,
            sender_status=InvoiceSenderStatusEnum.SENDER
        )

        self.session.add(invoice)
        self.session.commit()

        return invoice

    def create_invoice_billing(self, id: UUID, billing_id: UUID) -> InvoiceBillingSchemaOut:
        invoice = InvoiceBilling(
            invoice_id=id,
            billing_id=billing_id
        )

        self.session.add(invoice)
        self.session.commit()

        return invoice

    def get_invoice_id(self, id: UUID) -> InvoiceSchemaOut:
        return Invoice.query(self.session).filter(Invoice.id == id).first()

    def get_invoice_for_billing(self, billing_id: UUID) -> InvoiceBillingSchemaOut:
        return InvoiceBilling.query(self.session).filter(InvoiceBilling.billing_id == billing_id).first()

    def remove_invoice_billing(self, billing_id: UUID, invoice_id: UUID) -> bool:
        invoice_billing = InvoiceBilling.query(self.session).filter(
            InvoiceBilling.billing_id == billing_id,
            InvoiceBilling.invoice_id == invoice_id).first()

        self.session.delete(invoice_billing)
        self.session.commit()

        return True

    def invoice_exists_billing(self, invoice_id: UUID) -> InvoiceBillingSchemaOut:
        return InvoiceBilling.query(self.session).filter(InvoiceBilling.invoice_id == invoice_id).first()

    def update(self, invoice_in: InvoiceSchemaIn, invoice: Invoice) -> InvoiceSchemaOut:
        invoice.reference = invoice_in.reference
        invoice.status = invoice_in.status

        self.session.add(invoice)
        self.session.commit()

        return invoice

    def create_log(self, invoice_id: UUID, message: str) -> InvoiceLogSchemaOut:
        log = InvoiceLog(
            invoice_id=invoice_id,
            history=message
        )

        self.session.add(log)
        self.session.commit()

        return log

    def invoice_history(self, invoice_id: UUID) -> List[InvoiceLogSchemaOut]:
        return InvoiceLog.query(self.session).filter(InvoiceLog.invoice_id == invoice_id).all()

    def get_last_reference(self) -> InvoiceSchemaOut:
        return Invoice.query(self.session).filter(Invoice.company_id == self.current_user.company_id).order_by(Invoice.created_date.desc()).first()