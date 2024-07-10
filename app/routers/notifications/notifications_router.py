import os
from datetime import datetime
from typing import Annotated

import requests
from fastapi import APIRouter, Body, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.notifications.token import FcmToken
from app.services.authentication_service import check_authentication, get_user_id
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException

NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")

router = APIRouter()
security = HTTPBearer()


@router.post(
    "/notifications/update_fcm_token",
    tags=["Notifications"],
    status_code=201,
    description="Update user fcm token",
)
def update_user_avatar(
    token: FcmToken,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            response = requests.post(
                f"{NOTIFICATIONS_URL}/notifications/update_fcm_token",
                json={"user_id": user_id, "fcm_token": token.fcm_token},
            )
            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
