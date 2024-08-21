from app.constants.enums.permission_enum import PermissionEnum
from tests import get_client, run_test_with_try
from app.schemas.user_schemas import UserSchemaIn
from app.schemas.company_schemas import CompanySchemaIn
from app.utils.encoders import Encoder
import json

def create_user():   
  
    client = get_client()
    company = CompanySchemaIn(
        id="469264d5-6203-4f2e-aa2e-fdb0d939bc96",
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
    
    ret = client.post('/companies/', json=company.dict())
 
    
    company_ = ret.json()['id']
  

    user = UserSchemaIn(
        company_id=str(company_),
        fullname="John Connor",
        document="000.000.000-10",
        email="john.connor@skynet.com",
        permission=PermissionEnum.ADMIN,
        image_path=None,
        position="LEAD",
    )

    response = client.post('/users/', json=json.dumps(user.dict(), cls=Encoder))

    return response