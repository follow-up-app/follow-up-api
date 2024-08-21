import os
import sys
from starlette.testclient import TestClient
from main import app
from config import Settings, get_settings

sys.path.append(os.getcwd())


def delete_db():
    os.remove('./test.db')


def get_settings_override():
    return Settings(
        SQLALCHEMY_DATABASE_URI="sqlite:///./test.db",
        TESTING=True
    )


app.dependency_overrides[get_settings] = get_settings_override


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
            func()
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            delete_db()
        print("Finished test " + func.__name__)

    return function_wrapper
