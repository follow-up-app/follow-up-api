from typing import List
from schemas.company_schemas import CompanyIn
from tests import get_client, delete_db, run_test_with_try
from tests.auth_test import signup_user, admin_email, login, default_email



def create_company(token: str):
    company = CompanyIn(
        name = 'Company Test',
        document = '12345678910123',
        address='Street Test 123',
        zip_code = '00000-000',
        city='Florianópolis',
        state='SC',
        country='BRA',
        email='test@company.com',
        phone='554898486352'
    )
    client = get_client(token=token)
    response = client.post('/company', json=company.dict())
    print(response.content)

    return response

@run_test_with_try
def test_can_create_company():
    signup_user()
    token = login()
    response = create_company(token=token)
    assert response.status_code == 401

    signup_user(email=admin_email)
    token = login(email=admin_email)
    response = create_company(token=token)
    assert response.status_code == 200

