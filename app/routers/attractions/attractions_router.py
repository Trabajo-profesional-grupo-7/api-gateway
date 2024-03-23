from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *
from fastapi import APIRouter, Depends

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.autentication_service import check_authentication, get_user_id

from app.schemas.attractions_schemas.attractions import AttractionByID

from datetime import datetime

import requests

router = APIRouter()
security = HTTPBearer()

# Get attraction by id

@router.get(
    "/attractions/byid/{attraction_id}",
    status_code=200,
    tags=["Attractions"],
    description="Gets an attraction given its ID",
    response_model=AttractionByID,
)
def get_attraction(attraction_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"http://attractions:8003/attractions/byid/{attraction_id}",
            )

            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])

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
def search_attraction_by_text(attraction: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            data={
                "user_id": user_id,
                "query": attraction
            }
            response: Response = requests.post(
                f"http://attractions:8003/attractions/search", json=data,
            )

            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])

            attraction_info = response.json()
            return  attraction_info

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
def get_nearby_attractions(latitude: float, longitude:float, radius: float, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response: Response = requests.post(
                f"http://attractions:8003/attractions/nearby/{latitude}/{longitude}/{radius}",
            )

            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])

            attractions_info = response.json()
            return  attractions_info
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)

