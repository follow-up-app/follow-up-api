from app.core.rabbitmq import RabbitMQHandler
from app.schemas.schedule_schemas import ScheduleSchemaOut


class QueueService:
    def __init__(self):
        self.queue = RabbitMQHandler()

    def sender_payment(self, schedule: ScheduleSchemaOut) -> bool:
        self.queue.send_message(str(schedule.id))

        return True
