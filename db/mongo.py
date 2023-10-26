from pymongo import MongoClient
from config import get_settings
from fastapi import Depends
from uuid import UUID
from db.models import User, UserPermission
from sqlalchemy.orm import Session
import enum


class Type(enum.Enum):
    WELCOME: str = 'BOAS_VINDAS'
    PROFILE: str = 'PERFIL'
    SCHEDULE: str = 'AGENDA'
    RESULT: str = 'RESULTADO'


class Mongo:
    def __init__(self):
        settings = get_settings()
        client = MongoClient(settings.MONGO_DATABASE_URI)
        database = client['follow_up']
        self.collection = database['notifications']

    # USER EVENTS
    def welcome_app(self, user: User):
        notification = {
            'user_id':  str(user.id),
            'message': 'Bem-vindo ao Follow-UP!',
            'read': False,
            'type': Type.WELCOME,
            'uri': '/home'
        }
        self.collection.insert_one(notification)

        return True

    def update_password(self, user: User):
        notification = {
            'user_id':  str(user.id),
            'message': 'Você alterou sua senha de acesso!',
            'read': False,
            'type': Type.PROFILE.value,
            'uri': '/home'
        }
        self.collection.insert_one(notification)

        return True

    def create_schedule_notitification(self, user_id, event_id):
        notification = {
            'user_id':  str(user_id),
            'event_id': str(event_id),
            'message': 'Você tem um nova agenda',
            'read': False,
            'type': Type.SCHEDULE.value,
            'uri': '/scheduler'
        }
        self.collection.insert_one(notification)

        return True

    def update_schedule_notitification(self, user_id, event_id):
        notification = {
            'user_id':  str(user_id),
            'event_id': str(event_id),
            'message': 'Sua agenda sofreu alterações',
            'read': False,
            'type': Type.SCHEDULE.value,
            'uri': '/scheduler'
        }
        self.collection.insert_one(notification)

        return True

    def finish_schedule(self, user_id, event_id):
        notification = {
            'user_id':  str(user_id),
            'event_id': str(event_id),
            'message': 'Sua agenda foi finalizada',
            'read': False,
            'type': Type.SCHEDULE.value,
            'uri': '/scheduler'
        }
        self.collection.insert_one(notification)

        return True

    def generate_result(self, user_id, event_id):
        notification = {
            'user_id':  str(user_id),
            'event_id': str(event_id),
            'message': 'Novo resultado gerado',
            'read': False,
            'type': Type.RESULT.value,
            'uri': '/scheduler'
        }
        self.collection.insert_one(notification)

        return True

    # ADMIN EVENTS
    def create_event_admin(self, session: Session, event_id):
        users = User.query(session).filter(
            User.permission == UserPermission.ADMIN).all()

        for user in users:
            notification = {
                'user_id':  str(user.id),
                'event_id': str(event_id),
                'message': 'Nova agenda criada',
                'read': False,
                'type': Type.SCHEDULE.value,
                'uri': '/scheduler'
            }
            self.collection.insert_one(notification)

        return True

    def update_event_admin(self, session: Session, event_id):
        users = User.query(session).filter(
            User.permission == UserPermission.ADMIN).all()
        for user in users:
            notification = {
                'user_id':  str(user.id),
                'event_id': str(event_id),
                'message': 'Atualização de agenda',
                'read': False,
                'type': Type.SCHEDULE.value,
                'uri': '/scheduler'
            }
            self.collection.insert_one(notification)

        return True
    
    def finish_event_admin(self, session: Session, event_id):
        users = User.query(session).filter(
            User.permission == UserPermission.ADMIN).all()
        for user in users:
            notification = {
                'user_id':  str(user.id),
                'event_id': str(event_id),
                'message': 'Agenda finalizada',
                'read': False,
                'type': Type.SCHEDULE.value,
                'uri': '/scheduler'
            }
            self.collection.insert_one(notification)

        return True
    
    def generate_result_admin(self, session: Session, event_id):
        users = User.query(session).filter(
            User.permission == UserPermission.ADMIN).all()
        for user in users:
            notification = {
                'user_id':  str(user.id),
                'event_id': str(event_id),
                'message': 'Novo resultado gerado',
                'read': False,
                'type': Type.RESULT.value,
                'uri': '/scheduler'
            }
            self.collection.insert_one(notification)

        return True


    #NOTIFICATIONS
    def get_notifications(self, user_id):
        return list(self.collection.find({"user_id": str(user_id), "read": False}))

    def get_notifications_count(self, user_id):
        return list(self.collection.count_documents({"user_id": str(user_id), "read": False}))

    def read_notification(self, user_id):
        pass
