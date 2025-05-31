from tests import get_client, run_test_with_try
from tests.integrations.auth_test import login
from app.schemas.company_schemas import CompanySchemaIn, CompanySchemaOut
from app.constants.enums.company_enum import CompanyEnum


@run_test_with_try
def test_can_create_company():
    payload = CompanySchemaIn(
        fantasy_name="Skynet",
        social_name="Skynet SA",
        document="00.000.000/0001-10",
        address="Street X",
        number_address="25",
        complement=None,
        zip_code="99999-99",
        district="Ingleses",
        city="Florianópolis",
        state="SC",
        email="contact@skynet.org",
        phone="55548984863711",
        city_code="0001",
        aliquot=10,
        municipal_registration="000093",
        iss_retained=False,
        licences_n=50,
        api_nfes_token="AAIII"
    )
    token = login()
    client = get_client(token)
    response = client.post("/companies/", json=payload.dict())

    assert response.status_code == 200

    response_schema = CompanySchemaOut(**response.json())

    assert response_schema.fantasy_name == 'SKYNET'
    assert response_schema.social_name == 'SKYNET SA'
    assert response_schema.document == '00.000.000/0001-10'
    assert response_schema.email == 'contact@skynet.org'
    assert response_schema.phone == '55548984863711'
    assert response_schema.city == 'Florianópolis'
    assert response_schema.district == 'Ingleses'
    assert response_schema.city_code == '0001'
    assert response_schema.status == CompanyEnum.ACTIVE


# def test_can_edit_company():
#     payload = CompanySchemaIn(
#         id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
#         fantasy_name="Follow Up",
#         social_name="App Follow Up Ltda",
#         document="00.000.000/0001-00",
#         address="Street X",
#         number_address="25",
#         complement=None,
#         zip_code="99999-99",
#         district="Ingleses",
#         city="Florianópolis",
#         state="SC",
#         email="app@appfollowup.com",
#         phone="55548984863711",
#         city_code="0001",
#         aliquot=10,
#         municipal_registration="000093",
#         iss_retained=False,
#         licences_n=70,
#         api_nfes_token="AAIIISSS",
#         status=CompanyEnum.ACTIVE
#     )

#     token = login()
#     client = get_client(token)
#     response = client.patch("/companies/469264d5-6203-4f2e-aa2e-fdb0d939bc96", json=payload.dict())

#     assert response.status_code == 200
#     assert response.fantasy_name == 'Follow Up'
#     assert response.document == '00.000.000/0001-00'
#     assert response.email == 'app@appfollowup.com'
#     assert response.phone == '55548984863711'
#     assert response.city == 'Florianópolis'
#     assert response.district == 'Ingleses'
#     assert response.city_code == '0001'
#     assert response.licences_n == 70
#     assert response.api_nfes_token == 'AAIIISSS'
#     assert response.status == CompanyEnum.ACTIVE


