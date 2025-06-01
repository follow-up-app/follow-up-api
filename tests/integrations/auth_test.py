from tests import get_client, run_test_with_try


default_email: str = "app@appfollowup.com"
default_pass: str = "test"


def login():
    client = get_client()
    login_schema = dict(username=default_email, password=default_pass)
    response = client.post("/auth/", json=login_schema)
    assert response.status_code == 200
    return response.json().get("access_token")
