from typing import Optional

import requests
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.constants import *
from app.utils.api_exception import APIException

security = HTTPBearer()

def check_authentication(credentials: HTTPAuthorizationCredentials) -> Optional[bool]:
    try:
        response = requests.get(
            "http://users:8000/users/verify_id_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"}
        )

        if response.status_code == 200:
            return True
        else:
            raise APIException(code=INVALID_CREDENTIALS_ERROR, msg="INVALID_CREDENTIALS_ERROR")
    except requests.RequestException as e:
        raise APIException(code=CONNECTION_ERROR, msg="Error de conexión con el servidor de autenticación")

def get_user_id(credentials: HTTPAuthorizationCredentials) -> int:
    try:
        response = requests.get(
            "http://users:8000/users/verify_id_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"}
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(code=INVALID_CREDENTIALS_ERROR, msg="INVALID_CREDENTIALS_ERROR")
    except requests.RequestException as e:
        raise APIException(code=CONNECTION_ERROR, msg="Error de conexión con el servidor de autenticación")