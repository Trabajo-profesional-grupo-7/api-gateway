from typing import Annotated
import json

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.autentication import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.api_exception import *
from app.utils.constants import *

from app.schemas.autentication import Token
from app.schemas.users import User, UserCreate, UserLogin, UserId

import requests

router = APIRouter()
security = HTTPBearer()

# Auth

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
            "http://users:8000/users/refresh_token",
            headers={"Authorization": f"Bearer {credentials.credentials}"}
        )

        if response.status_code == 401:
            raise APIException(code=USER_UNAUTHORIZED_ERROR, msg=response.json()["detail"])
        tokens = response.json()

        return Token.model_construct(
        token=tokens["token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        )
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

        response = requests.post(
            "http://users:8000/users/signup",
            json=user_data
        )

        if response.status_code == 409:
            raise APIException(code=USER_EXISTS_ERROR, msg="Email already used")
        elif not response.ok:
            raise APIException(code=response.status_code, msg=response.text)

        response_data = response.json()

        return User.model_construct(
            username=response_data["username"],
            email=response_data["email"],
            birth_date=response_data["birth_date"],
            preferences=response_data["preferences"],
            id=response_data["id"],
        )
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
        
        response = requests.post(
            "http://users:8000/users/login",
            json=user_data
        )

        if response.status_code == 400:
            raise APIException(code=LOGIN_ERROR, msg="LOGIN_ERROR")
        
        tokens = response.json()
    
        return Token.model_construct(
            token=tokens["token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )

    except APIException as e:
        raise APIExceptionToHTTP().convert(e)