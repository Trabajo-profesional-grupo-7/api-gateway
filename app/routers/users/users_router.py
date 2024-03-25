from datetime import datetime

import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.users_schemas.users import User, UserBase
from app.services.autentication_service import check_authentication
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *

router = APIRouter()
security = HTTPBearer()

# Get user


@router.get(
    "/users",
    tags=["Users"],
    status_code=200,
    response_model=User,
    description="Get user profile",
)
def get_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response = requests.get(
                "http://users:8000/users",
                headers={"Authorization": f"Bearer {credentials.credentials}"},
            )

            handle_response_error(200, response)

            response_data = response.json()

            return User.model_construct(
                username=response_data["username"],
                email=response_data["email"],
                birth_date=datetime.fromisoformat(response_data["birth_date"]).date(),
                preferences=response_data["preferences"],
                id=response_data["id"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Update User


@router.patch(
    "/users",
    tags=["Users"],
    status_code=200,
    response_model=User,
    description="Update user profile",
)
def update_user_profile(
    updatedUser: UserBase, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):
            response = requests.patch(
                "http://users:8000/users",
                json=updatedUser.dict(),
                headers={"Authorization": f"Bearer {credentials.credentials}"},
            )

            handle_response_error(200, response)

            response_data = response.json()

            return User.model_construct(
                username=response_data["username"],
                email=response_data["email"],
                birth_date=datetime.fromisoformat(response_data["birth_date"]).date(),
                preferences=response_data["preferences"],
                id=response_data["id"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Delete user


@router.delete(
    "/users",
    tags=["Users"],
    status_code=200,
    response_model=User,
    description="Delete user profile",
)
def delete_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response = requests.delete(
                "http://users:8000/users",
                headers={"Authorization": f"Bearer {credentials.credentials}"},
            )

            handle_response_error(200, response)

            response_data = response.json()

            return User.model_construct(
                username=response_data["username"],
                email=response_data["email"],
                birth_date=datetime.fromisoformat(response_data["birth_date"]).date(),
                preferences=response_data["preferences"],
                id=response_data["id"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
