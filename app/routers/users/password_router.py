from datetime import datetime
from typing import Annotated

import requests
from app.schemas.users_schemas.password import (
    InitRecoverPassword,
    PasswordRecover,
    UpdatePassword,
)
from app.services.autentication_service import check_authentication
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import APIException, APIExceptionToHTTP
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


# UPDATE PASSWORD


@router.patch(
    "/users/password/update",
    tags=["Password"],
    status_code=200,
    description="Receives the current and new passwords and updates it if the current password is correct",
)
def update_password(
    update_data: UpdatePassword,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        if check_authentication(credentials):

            response = requests.patch(
                "http://users:8000/users/password/update",
                json=update_data.dict(),
                headers={
                    "Authorization": f"{credentials.scheme} {credentials.credentials}"
                },
            )

            handle_response_error(200, response)

            new_password = response.json()

            return response.json()

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# RECOVER PASSWORD


@router.post(
    "/users/password/recover",
    tags=["Password"],
    status_code=200,
    response_model=PasswordRecover,
    description="Send code by email to recover the password",
)
def init_recover_password(
    recover_data: InitRecoverPassword,
):
    try:

        response = requests.post(
            "http://users:8000/users/password/recover",
            json=recover_data.dict(),
        )

        handle_response_error(200, response)

        recover = response.json()

        return PasswordRecover.model_construct(
            user_id=recover["user_id"],
            emited_datetime=recover["emited_datetime"].isoformat(),
            leftover_attempts=recover["leftover_attempts"],
        )

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
