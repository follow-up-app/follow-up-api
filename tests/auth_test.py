import os

from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session

from db import get_db
from db.models import User, UserPermission
from main import app
from schemas.user_schemas import UserRegisterSchemaIn
from tests import get_client, get_settings_override, delete_db, run_test_with_try



default_email: str = "user@email.com"
default_name: str = "Full name of user"
admin_email = "admin@icontact.com"


def signup_user(email: str = default_email, name: str = default_name):
    client = get_client()
    login_schema = UserRegisterSchemaIn(
        email=email,
        password="123456",
        fullname=name
    )
    json = login_schema.dict()
    response = client.post("/users/register/", json=json)

    assert response.status_code == 200
    return response.json().get('access_token')


def login(email: str = default_email):
    client = get_client()
    login_schema = dict(email=email, password='123456')
    response = client.post('/users/login/', json=login_schema)
    assert response.status_code == 200
    return response.json().get('access_token')

@run_test_with_try
def test_login():
    signup_user()
    login()

@run_test_with_try
def test_signup():
    signup_user()
    
@run_test_with_try
def test_user_recovery(email: str = default_email):
    
    signup_user()
    client = get_client()
    response = client.post(f'/users/recovery-password/', json=dict(email=email))
    assert response.status_code == 200

    new_password = "654321"
    settings = get_settings_override()
    ts = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = ts.dumps(email, salt='recover-key')

    response = client.post(f'/users/reset/', json=dict(password=new_password, token=token))
    assert response.status_code == 200

    login_schema = dict(email=email, password=new_password)
    response = client.post('/users/login/', json=login_schema)
    assert response.status_code == 200
