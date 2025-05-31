import os
import sys
from starlette.testclient import TestClient
from main import app
from config import Settings, get_settings
from db.models import Company, User
from app.constants.enums.company_enum import CompanyEnum
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from db import get_db
from app.core.security import hash_password

sys.path.append(os.getcwd())
settings = get_settings()

def delete_db():
    os.remove('./test.db')

def get_settings_override():
    return Settings(
        SQLALCHEMY_DATABASE_URI="sqlite:///./test.db",
        TESTING=True
    )

app.dependency_overrides[get_settings] = get_settings_override

db_gen = get_db(get_settings_override())
session = next(db_gen) 


def creates_start_test():
    company = Company(
        id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
        fantasy_name="Follow Up",
        social_name="App Follow Up Ltda",
        document="00.000.000/0001-00",
        address="Street X",
        number_address="25",
        complement=None,
        zip_code="99999-99",
        district="Ingleses",
        city="Florianópolis",
        state="SC",
        email="app@appfollowup.com",
        phone="55548984863711",
        city_code="0001",
        aliquot=10,
        municipal_registration="000093",
        iss_retained=False,
        licences_n=50,
        api_nfes_token="AAIII",
        status=CompanyEnum.ACTIVE
    )

    session.add(company)
    session.commit()

    user = User(
        company_id=company.id,
        fullname='Integratrion Test',
        password_hash=hash_password('test'),
        email='app@appfollowup.com',
        document='000.000.000-12',
        permission=PermissionEnum.ADMIN,
        position='TESTER',
        status=StatusEnum.ACTIVE,
    )

    session.add(user)
    session.commit()

def get_client(token: str = None) -> TestClient:
    client = TestClient(app)
    if token:
        client.headers = {
            'Authorization': 'Bearer ' + token
        }
    return client


def run_test_with_try(func):
    def function_wrapper():
        print("Starting test " + func.__name__)
        try:
            creates_start_test()
            func()
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            delete_db()
        print("Finished test " + func.__name__)

    return function_wrapper
