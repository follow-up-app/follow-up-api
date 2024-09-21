from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader
import os
from config import get_settings
from db.models import User
import logging
from fastapi import HTTPException
from app.core.crypt import Crypt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mailer:
    def __init__(self):
        self._settings = get_settings()
        self.path: str = '%s/public/templates/' % os.getcwd()
        self.env = Environment(loader=FileSystemLoader(self.path))
        self.image_path = os.path.join(self.path, 'img', 'follow_up.png')

    def welcome_user(self, user: User):
        message = MIMEMultipart()
        message['subject'] = 'Follow UP | app -Bem-vindo ao Follow-Up'
        message['From'] = self._settings.SMTP_EMAIL_FROM
        message['To'] = user.email

        token = Crypt.encrypt(user.id, user.email)
        print('-a')
        body_content = self.env.get_template('welcome.html')

        print('a')
        body_content = body_content.render(
            data=user, url=self._settings.PANEL_URL, token=token, image='templates/img/follow_up.png')
        message.attach(MIMEText(body_content, "html"))

        with open(self.image_path, 'rb') as file:
            image_data = file.read()
            image = MIMEImage(
                image_data, name=os.path.basename(self.image_path))
            image.add_header('Content-ID', '<image_file>')
            message.attach(image)

        self.sender(user.email, message)

    def recovery_password(self, user: User):
        message = MIMEMultipart()
        message['subject'] = 'Follow UP | app -Recuperação de Senha'
        message['From'] = self._settings.SMTP_EMAIL_FROM
        message['To'] = user.email

        token = Crypt.encrypt(user.id, user.email)

        body_content = self.env.get_template('recovery.html')
        body_content = body_content.render(
            data=user, url=self._settings.PANEL_URL, token=token, image='templates/img/follow_up.png')
        message.attach(MIMEText(body_content, "html"))

        with open(self.image_path, 'rb') as file:
            image_data = file.read()
            image = MIMEImage(
                image_data, name=os.path.basename(self.image_path))
            image.add_header('Content-ID', '<image_file>')
            message.attach(image)

        self.sender(user.email, message)

    def sender(self, email, message):
        try:
            print('b')
            server = SMTP_SSL(self._settings.SMTP_HOST,
                              self._settings.SMTP_PORT)
            server.login(self._settings.SMTP_EMAIL_FROM,
                         self._settings.SMTP_EMAIL_PASSWORD)
            server.sendmail(self._settings.SMTP_EMAIL_FROM,
                            email, message.as_string())
            server.quit()

        except Exception as e:
            logger.error(f"Error in sender email: {e}")
            raise HTTPException(status_code=500, detail='Server error')
