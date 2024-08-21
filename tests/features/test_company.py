from tests import get_client, run_test_with_try
from app.schemas.company_schemas import CompanySchemaIn


def create_company():
    company = CompanySchemaIn(
        name="Skynet SA",
        document="00.000.000/0001-00",
        address="Street X",
        number_address="25",
        complement=None,
        zip_code="99999-99",
        city="Florianópolis",
        state="SC",
        country="Brazil",
        email="contact@skynet.org",
        phone="55548984863711"
    )
    client = get_client()
    response = client.post('/companies/', json=company.dict())

    return response


@run_test_with_try
def test_can_create_company():
    response = create_company()
    assert response.status_code == 200

    response = create_company()
    assert response.status_code == 400


@run_test_with_try
def test_can_all_companies():
    client = get_client()
    response = client.get('/companies/')
    assert response.status_code == 200


@run_test_with_try
def test_id_company():
    create = create_company()
    company_id = create.json()["id"]
    client = get_client()
    response = client.get('/companies/' + str(company_id))
    assert response.status_code == 200
