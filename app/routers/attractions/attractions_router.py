import os
from typing import List, Optional

import requests
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.attractions_schemas.attractions import (
    AttractionByID,
    AttractionByText,
    AutocompleteAttractions,
    ScheduleAttraction,
    SearchAttractionByText,
)
from app.services.authentication_service import check_authentication, get_user_id
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *

ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")

router = APIRouter()
security = HTTPBearer()

###################
#    METADATA     #
###################


@router.get(
    "/metadata",
    status_code=200,
    tags=["Metadata"],
    description="Gets tha application metadata",
)
def get_metadata():
    try:
        response = requests.get(f"{ATTRACTIONS_URL}/metadata")

        handle_response_error(201, response)

        return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#     SEARCH      #
###################

# Get attraction by id


@router.get(
    "/attractions/byid/{attraction_id}",
    status_code=200,
    tags=["Search Attractions"],
    description="Gets an attraction given its ID",
)
def get_attraction(
    attraction_id: str,
    user_id: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            params = {}

            if user_id and user_id == get_user_id(credentials):
                params["user_id"] = user_id

            response = requests.get(
                f"{ATTRACTIONS_URL}/attractions/byid/{attraction_id}", params=params
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Get attraction by text


@router.post(
    "/attractions/search",
    status_code=201,
    tags=["Search Attractions"],
    description="Searches attractions given a text query",
)
def search_attraction_by_text(
    attraction: SearchAttractionByText,
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            params = {}
            if user_id and user_id == get_user_id(credentials):
                params["user_id"] = user_id
            if type:
                params["type"] = type

            data = {"query": attraction.attraction_name}
            response: Response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/search",
                json=data,
                params=params,
            )

            handle_response_error(201, response)

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
    tags=["Search Attractions"],
    description="Gets nearby attractions given a latitude and longitude",
)
def get_nearby_attractions(
    latitude: float,
    longitude: float,
    radius: float,
    user_id: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            params = {}

            if user_id and user_id == get_user_id(credentials):
                params["user_id"] = user_id

            response: Response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/nearby/{latitude}/{longitude}/{radius}",
                params=params,
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Search by recommendation


@router.get(
    "/attractions/recommendations/{attraction_id}",
    status_code=201,
    tags=["Search Attractions"],
    description="Gets similar attractions given an attraction ID",
)
def get_attraction_recommendations(
    attraction_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    page: int = Query(0, description="Page number", ge=0),
    size: int = Query(10, description="Number of items per page", ge=1, le=100),
):
    try:
        if check_authentication(credentials):
            response: Response = requests.get(
                f"{ATTRACTIONS_URL}/attractions/recommendations/{attraction_id}?page={page}&size={size}",
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#  AUTOCOMPLETE   #
###################


@router.post(
    "/attractions/autocomplete",
    status_code=201,
    tags=["Search Attractions"],
    description="Returns attractions predictions given a substring. Can filter by a list of attraction types.",
)
def autocomplete_attractions(
    data: AutocompleteAttractions,
    attraction_types: List[str] = Query(
        None,
        title="Attraction Types",
        description="Filter by attraction types",
    ),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            params = {"query": data.attraction_name}

            if attraction_types:
                params["attraction_types"] = ",".join(attraction_types)

            response: Response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/autocomplete",
                json=params,
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#    RUN SYSTEM   #
###################


@router.post(
    "/attractions/run-recommendation-system",
    status_code=201,
    tags=["Search Attractions"],
    description="Runs the recommendation system",
)
def run_recommendation_system(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            response: Response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/run-recommendation-system",
            )

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

            response = requests.post(f"{ATTRACTIONS_URL}/attractions/save", json=data)

            handle_response_error(201, response)

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
                f"{ATTRACTIONS_URL}/attractions/unsave", json=data
            )

            handle_response_error(204, response)

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
                f"{ATTRACTIONS_URL}/attractions/save-list?user_id={current_user_id}&page={page}&size={size}",
            )

            handle_response_error(200, response)

            return response.json()
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

            response = requests.post(f"{ATTRACTIONS_URL}/attractions/like", json=data)

            handle_response_error(201, response)

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
                f"{ATTRACTIONS_URL}/attractions/unlike", json=data
            )

            handle_response_error(204, response)

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
                f"{ATTRACTIONS_URL}/attractions/like-list?user_id={current_user_id}&page={page}&size={size}",
            )

            handle_response_error(200, response)

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

            response = requests.post(f"{ATTRACTIONS_URL}/attractions/done", json=data)

            handle_response_error(201, response)

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
                f"{ATTRACTIONS_URL}/attractions/undone", json=data
            )

            handle_response_error(204, response)
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
                f"{ATTRACTIONS_URL}/attractions/done-list?user_id={current_user_id}&page={page}&size={size}",
            )

            handle_response_error(200, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#      RATE       #
###################


@router.post(
    "/attractions/rate",
    status_code=201,
    tags=["Rate Attraction"],
    description="Rates an attraction by an user",
)
def rate_attraction(
    attraction_id: str,
    rating: int = Query(5, description="Rating must be between 1 and 5"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {
                "user_id": current_user_id,
                "attraction_id": attraction_id,
                "rating": rating,
            }

            response = requests.post(f"{ATTRACTIONS_URL}/attractions/rate", json=data)

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#     COMMENT     #
###################

# ADD COMMENT


@router.post(
    "/attractions/comment",
    status_code=201,
    tags=["Comment Attraction"],
    description="Comments an attraction for an user",
)
def comment_attraction(
    attraction_id: str,
    comment: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            current_user_id = get_user_id(credentials)

            data = {
                "user_id": current_user_id,
                "attraction_id": attraction_id,
                "comment": comment,
            }

            response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/comment", json=data
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# DELETE COMMENT


@router.delete(
    "/attractions/comment",
    status_code=204,
    tags=["Comment Attraction"],
    description="Deletes a comment by comment_id",
)
def delete_comment(
    comment_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):

            data = {"comment_id": comment_id}

            response = requests.delete(
                f"{ATTRACTIONS_URL}/attractions/comment", json=data
            )

            handle_response_error(204, response)
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# UPDATE COMMENT


@router.put(
    "/attractions/comment",
    status_code=201,
    tags=["Comment Attraction"],
    description="Edits a comment by comment_id",
)
def update_comment(
    comment_id: int,
    new_comment: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            data = {"comment_id": comment_id, "new_comment": new_comment}

            response = requests.put(f"{ATTRACTIONS_URL}/attractions/comment", json=data)

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###################
#     SCHEDULE    #
###################

# SCHEDULED


@router.post(
    "/attractions/scheduled",
    status_code=201,
    tags=["Schedule Attraction"],
    description="Schedules an attraction for a user at a certain timestamp",
)
def schedule_attraction(
    data: ScheduleAttraction,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            attraction_scheduled = data.dict()
            attraction_scheduled["user_id"] = get_user_id(credentials)

            attraction_scheduled["scheduled_time"] = attraction_scheduled[
                "scheduled_time"
            ].isoformat()

            response = requests.post(
                f"{ATTRACTIONS_URL}/attractions/scheduled",
                json=attraction_scheduled,
            )

            handle_response_error(201, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# UNSCHEDULED


@router.delete(
    "/attractions/unschedule",
    status_code=204,
    tags=["Schedule Attraction"],
    description="Unschedules an attraction for a user",
)
def unschedule_attraction(
    attraction_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            user_id = get_user_id(credentials)
            unscheduled_attraction = {
                "user_id": user_id,
                "attraction_id": attraction_id,
            }

            response = requests.delete(
                f"{ATTRACTIONS_URL}/attractions/unschedule",
                json=unscheduled_attraction,
            )

            handle_response_error(204, response)

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# SCHEDULED LIST
@router.get(
    "/attractions/scheduled-list",
    status_code=200,
    tags=["Schedule Attraction"],
    description="Returns a list of the attractions scheduled by an user",
)
def get_scheduled_attractions_list(
    page: int = Query(0, description="Page number", ge=0),
    size: int = Query(10, description="Number of items per page", ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):

            user_id = get_user_id(credentials)

            response = requests.get(
                f"{ATTRACTIONS_URL}/attractions/scheduled-list",
                params={"user_id": user_id, "page": page, "size": size},
            )

            handle_response_error(200, response)

            return response.json()
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
