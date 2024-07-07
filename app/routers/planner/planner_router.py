import os

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.routers.planner.planner_queue import queue_plan
from app.schemas.planner_schemas.planner import PlanMetaData
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


@router.get("/plan/user/{id}", tags=["Planner"])
def get_plan(id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response = requests.get(f"{PLANNER_URL}/plan/user/{id}")

            handle_response_error(200, response)

            return response.json()
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
