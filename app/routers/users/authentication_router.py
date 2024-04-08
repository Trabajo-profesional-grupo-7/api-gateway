import os
from datetime import datetime
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.users_schemas.autentication import *
from app.schemas.users_schemas.users import User, UserCreate, UserId, UserLogin
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")

router = APIRouter()
security = HTTPBearer()

# Auth


@router.get(
    "/users/verify_id_token",
    tags=["Auth"],
    status_code=200,
    description="Authenticate user by the jwt token",
)
def verify_id_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        response = requests.get(
            f"{AUTHENTICATION_URL}/users/verify_id_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )

        handle_response_error(200, response)

        authenticated_id = response.json()

        return UserId.model_construct(id=int(authenticated_id))
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.post(
    "/users/refresh_token",
    tags=["Auth"],
    status_code=200,
    response_model=Token,
    description="Refresh user token",
)
def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        response = requests.post(
            f"{AUTHENTICATION_URL}/users/refresh_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )

        handle_response_error(200, response)

        tokens = response.json()

        return Token.model_construct(
            token=tokens["token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Sign up


@router.post(
    "/users/signup",
    tags=["Auth"],
    status_code=201,
    response_model=User,
    description="Create a new user in the database",
)
def create_user(user: UserCreate):
    try:
        user_data = {
            "username": user.username,
            "email": user.email,
            "birth_date": user.birth_date.isoformat(),
            "preferences": user.preferences,
            "password": user.password,
        }

        response = requests.post(f"{AUTHENTICATION_URL}/users/signup", json=user_data)

        handle_response_error(201, response)

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


# LogIn


@router.post(
    "/users/login",
    tags=["Auth"],
    status_code=200,
    response_model=Token,
    description="Generate a token for valid credentials",
)
def login_user(user: UserLogin):
    try:
        user_data = {
            "email": user.email,
            "password": user.password,
        }

        response = requests.post(f"{AUTHENTICATION_URL}/users/login", json=user_data)

        handle_response_error(200, response)

        tokens = response.json()

        return Token.model_construct(
            token=tokens["token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
