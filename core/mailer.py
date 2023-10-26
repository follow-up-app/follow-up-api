from requests.sessions import session
import io
from fastapi.param_functions import File
from db import get_db
from fastapi import Depends
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from sqlalchemy.orm.session import Session
from config import Settings, get_settings
from db.models import User


class Mailer:
    def __init__(self):
        self._settings = get_settings()
        path: str = '%s/templates/' % os.getcwd()
        self.env = Environment(loader=FileSystemLoader(path))
        
        
    def welcome_user(self, user: User):
        message = MIMEMultipart()
        message['subject'] = 'Follow UP|app - Bem-vindo ao Follow-UP'
        message['From'] = self._settings.SMTP_EMAIL_FROM
        message['To'] = user.email
        body_content = self.env.get_template('welcome.html')
        body_content = body_content.render(data=user)
        message.attach(MIMEText(body_content, "html"))
        msg_body = message.as_string()
        server = SMTP(self._settings.SMTP_HOST, self._settings.SMTP_PORT)
        server.starttls()
        server.login(self._settings.SMTP_EMAIL_FROM,
                        self._settings.SMTP_EMAIL_PASSWORD)
        server.sendmail(self._settings.SMTP_EMAIL_FROM, user.email, msg_body)
        server.quit()
        
        
    
    def recovery_password(self, user: User):
        message = MIMEMultipart()
        message['subject'] = 'Follow UP|app -Recuperação de Senha'
        message['From'] = self._settings.SMTP_EMAIL_FROM
        message['To'] = user.email
        body_content = self.env.get_template('recovery.html')
        body_content = body_content.render(data=user)
        message.attach(MIMEText(body_content, "html"))
        msg_body = message.as_string()
        server = SMTP(self._settings.SMTP_HOST, self._settings.SMTP_PORT)
        server.starttls()
        server.login(self._settings.SMTP_EMAIL_FROM,
                        self._settings.SMTP_EMAIL_PASSWORD)
        server.sendmail(self._settings.SMTP_EMAIL_FROM, user.email, msg_body)
        server.quit()
        
        
    def send_generic_message(self, to: str, subject:str, template:str, data:dict)->None:
        message = MIMEMultipart()
        message['subject'] = subject
        message['From'] = self._settings.SMTP_EMAIL_FROM
        message['To'] = to
        body_content = self.env.get_template(template)
        body_content = body_content.render(data=data)
        message.attach(MIMEText(body_content, "html"))
        msg_body = message.as_string()
        server = SMTP(self._settings.SMTP_HOST, self._settings.SMTP_PORT)
        server.starttls()
        server.login(self._settings.SMTP_EMAIL_FROM,
                        self._settings.SMTP_EMAIL_PASSWORD)
        server.sendmail(self._settings.SMTP_EMAIL_FROM, to, msg_body)
        server.quit()