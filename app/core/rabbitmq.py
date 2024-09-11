import logging
import pika
from app.repositories.payment_repository import PaymnentRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.services.payment_service import PaymentService
from config import get_settings
from config import get_settings
from sqlalchemy.orm import Session

from db import get_db


class RabbitMQHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        settings = get_settings()
        self.url = settings.RABBITMQ_URL
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)

        session: Session = next(get_db(get_settings()))
        schedule_repository = ScheduleRepository(
            session=session, current_user=None)
        payment_repository = PaymnentRepository(
            session=session, current_user=None)
        self.payment_service = PaymentService(
            payment_repository=payment_repository, schedule_repository=schedule_repository)

        try:
            self.channel = self.connection.channel()
            self.queue = 'generate_payments'
            self.channel.queue_declare(queue=self.queue)

        except Exception as e:
            self.logger.error(f"Error in connect server queue: {e}")

    def send_message(self, message) -> bool:
        try:
            self.channel.basic_publish(
                exchange='', routing_key=self.queue, body=message)
            print(message)
            return True

        except Exception as e:
            self.logger.error(f"Error in sender queue payment: {e}")

    def listener(self):
        def callback(ch, method, properties, body):
            try:
                self.payment_service.create(body.decode())
            except Exception as e:
                self.logger.error(f"Error in process generate payment: {e}")

        try:
            self.channel.basic_consume(
                queue=self.queue, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
                self.logger.error(f"Error in process queue generate payment: {e}")