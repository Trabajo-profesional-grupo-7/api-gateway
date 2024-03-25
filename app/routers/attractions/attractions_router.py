from datetime import datetime

import requests
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.attractions_schemas.attractions import AttractionByID
from app.services.autentication_service import check_authentication, get_user_id
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *

router = APIRouter()
security = HTTPBearer()

###################
#       GET       #
###################

# Get attraction by id


@router.get(
    "/attractions/byid/{attraction_id}",
    status_code=200,
    tags=["Attractions"],
    description="Gets an attraction given its ID",
    response_model=AttractionByID,
)
def get_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"http://attractions:8003/attractions/byid/{attraction_id}",
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            attraction_info = response.json()
            return AttractionByID.model_construct(
                id=attraction_info["id"],
                displayName=attraction_info["displayName"],
                likes_count=attraction_info["likes_count"],
                saved_count=attraction_info["saved_count"],
                done_count=attraction_info["done_count"],
                avg_rating=attraction_info["avg_rating"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Get attraction by text


@router.post(
    "/attractions/search",
    status_code=200,
    tags=["Attractions"],
    description="Searches attractions given a text query",
)
def search_attraction_by_text(
    attraction: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            data = {"user_id": user_id, "query": attraction}
            response: Response = requests.post(
                f"http://attractions:8003/attractions/search",
                json=data,
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            attraction_info = response.json()
            return attraction_info

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Search attractions by coordinates


@router.post(
    "/attractions/nearby/{latitude}/{longitude}/{radius}",
    status_code=201,
    tags=["Get Attractions"],
    description="Gets nearby attractions given a latitude and longitude",
)
def get_nearby_attractions(
    latitude: float,
    longitude: float,
    radius: float,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response: Response = requests.post(
                f"http://attractions:8003/attractions/nearby/{latitude}/{longitude}/{radius}",
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            attractions_info = response.json()
            return attractions_info
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#      SAVE       #
###################
# Save attraction


@router.post(
    "/attractions/save",
    status_code=200,
    tags=["Save Attraction"],
    description="Saves an attraction for a user",
)
def save_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {
                "user_id": current_user_id,
                "attraction_id": attraction_id,
            }

            response = requests.post(
                f"http://attractions:8003/attractions/save", json=data
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            attractions_info = response.json()
            return attractions_info
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Unsave attraction


@router.delete(
    "/attractions/unsave",
    status_code=204,
    tags=["Save Attraction"],
    description="Unsaves an attraction for a user",
)
def unsave_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {
                "user_id": current_user_id,
                "attraction_id": attraction_id,
            }

            response = requests.delete(
                f"http://attractions:8003/attractions/unsave", json=data
            )

            if response.status_code != 204:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Get saved attractions


@router.get(
    "/attractions/save-list",
    status_code=200,
    tags=["Save Attraction"],
    description="Returns a list of the attractions saved by an user",
)
def get_saved_attractions_list(
    page: int = Query(0, description="Page number", ge=0),
    size: int = Query(10, description="Number of items per page", ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            response = requests.get(
                f"http://attractions:8003/attractions/save-list?user_id={current_user_id}&page={page}&size={size}",
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#      LIKE       #
###################

# LIKE


@router.post(
    "/attractions/like",
    status_code=201,
    tags=["Like Attraction"],
    description="Likes an attraction for a user",
)
def like_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {"user_id": current_user_id, "attraction_id": attraction_id}

            response = requests.post(
                f"http://attractions:8003/attractions/like", json=data
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# UNLIKE


@router.delete(
    "/attractions/unlike",
    status_code=204,
    tags=["Like Attraction"],
    description="Unlikes an attraction for a user",
)
def unlike_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {"user_id": current_user_id, "attraction_id": attraction_id}

            response = requests.delete(
                f"http://attractions:8003/attractions/unlike", json=data
            )

            if response.status_code != 204:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# ATTRACTIONS SAVED


@router.get(
    "/attractions/like-list",
    status_code=200,
    tags=["Like Attraction"],
    description="Returns a list of the attractions liked by an user",
)
def get_liked_attractions_list(
    page: int = Query(0, description="Page number", ge=0),
    size: int = Query(10, description="Number of items per page", ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            response = requests.get(
                f"http://attractions:8003/attractions/like-list?user_id={current_user_id}&page={page}&size={size}",
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#      DONE       #
###################

# DONE


@router.post(
    "/attractions/done",
    status_code=201,
    tags=["Done Attraction"],
    description="Marks as done a attraction for a user",
)
def mark_as_done_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {"user_id": current_user_id, "attraction_id": attraction_id}

            response = requests.post(
                f"http://attractions:8003/attractions/done", json=data
            )

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# UNDONE


@router.delete(
    "/attractions/undone",
    status_code=204,
    tags=["Done Attraction"],
    description="Marks as undone an attraction for a user",
)
def mark_as_undone_attraction(
    attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {"user_id": current_user_id, "attraction_id": attraction_id}

            response = requests.delete(
                f"http://attractions:8003/attractions/undone", json=data
            )

            if response.status_code != 204:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# ATTRACTIONS DONE LIST


@router.get(
    "/attractions/done-list",
    status_code=200,
    tags=["Done Attraction"],
    description="Returns a list of the attractions done by an user",
)
def get_done_attractions_list(
    page: int = Query(0, description="Page number", ge=0),
    size: int = Query(10, description="Number of items per page", ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            response = requests.get(
                f"http://attractions:8003/attractions/done-list?user_id={current_user_id}&page={page}&size={size}",
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()["detail"]
                )

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
