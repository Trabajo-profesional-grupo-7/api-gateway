from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.autentication import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.api_exception import *
from app.utils.constants import *

from app.schemas.autentication import *

import requests

router = APIRouter()
security = HTTPBearer()

@router.get(
    "/users/verify_id_token",
    tags=["Auth"],
    status_code=200,
    description="Authenticate user by the jwt token",
)
def verify_id_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        response = requests.get(
            "http://users:8000/users/verify_id_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"}
        )

        if response.status_code != 200:
            raise APIException(code=INVALID_CREDENTIALS_ERROR, msg="INVALID_CREDENTIALS_ERROR")

        authenticated_id = response.json()

        return UserId.model_construct(
            id=int(authenticated_id)
        )
        
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)

