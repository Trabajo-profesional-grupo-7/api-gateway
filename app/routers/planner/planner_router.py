import os

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.routers.planner.planner_queue import queue_plan
from app.schemas.planner_schemas.planner import AttractionPlan, PlanMetaData
from app.services.authentication_service import check_authentication, get_user_id
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import APIException, APIExceptionToHTTP

PLANNER_URL = os.getenv("PLANNER_URL")

router = APIRouter()
security = HTTPBearer()


@router.post("/plan", tags=["Planner"])
def create_plan(
    plan_metadata: PlanMetaData,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            queue_plan(user_id, plan_metadata)

            return "Plan queued"
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.get("/plan/user", tags=["Planner"])
def get_plan(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            response = requests.get(f"{PLANNER_URL}/plan/user/{user_id}")

            handle_response_error(200, response)

            return response.json()
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.get(
    "/plan/{plan_id}",
    tags=["Planner"],
    description="Get plan by id",
    status_code=200,
)
def get_plan_by_id(
    plan_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        if check_authentication(credentials):
            response = requests.get(f"{PLANNER_URL}/plan/{plan_id}")

            handle_response_error(200, response)

            return response.json()
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.delete(
    "/plan/attraction",
    tags=["Planner"],
    description="Delete attraction from a plan",
    status_code=200,
)
def delete_attraction(
    attraction: AttractionPlan,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.delete(
                f"{PLANNER_URL}/plan/attraction", json=attraction.dict()
            )

            handle_response_error(200, response)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.patch(
    "/plan/attraction",
    tags=["Planner"],
    description="Update attraction from a plan",
    status_code=200,
)
def update_attraction(
    attraction: AttractionPlan,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.patch(
                f"{PLANNER_URL}/plan/attraction", json=attraction.dict()
            )

            handle_response_error(200, response)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.delete(
    "/plan/{plan_id}",
    tags=["Planner"],
    description="Delete plan",
    status_code=200,
)
def delete_plan(
    plan_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.delete(f"{PLANNER_URL}/plan/{plan_id}")

            handle_response_error(200, response)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
