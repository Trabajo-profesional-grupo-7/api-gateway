import os
from datetime import date
from typing import Optional

import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.external_services_schemas.chatbot import AssistantResponse, ChatMessage
from app.schemas.external_services_schemas.cities import Cities
from app.schemas.external_services_schemas.currency import Currency
from app.schemas.external_services_schemas.flights import FlightInfo
from app.schemas.external_services_schemas.weather import FiveDayWeather
from app.services.authentication_service import check_authentication, get_user_id
from app.services.external_services.cities_services import parse_cities
from app.services.external_services.weather_services import parse_weather_days
from app.services.handle_error_service import handle_response_error
from app.utils.api_exception import *
from app.utils.constants import *

EXTERNAL_SERVICES_URL = os.getenv("EXTERNAL_SERVICES_URL")

router = APIRouter()
security = HTTPBearer()

# Flight


@router.get("/flights/status", tags=["Flights"])
async def flight_information(
    carrier_code: str,
    flight_number: str,
    departure_date: date,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"{EXTERNAL_SERVICES_URL}/flights/status",
                params={
                    "carrier_code": carrier_code,
                    "flight_number": flight_number,
                    "departure_date": departure_date,
                },
            )

            handle_response_error(200, response)

            response_data = response.json()

            return FlightInfo.model_construct(
                flight_departure_date=response_data["flight_departure_date"],
                flight_departure_time=response_data["flight_departure_time"],
                flight_arrival_date=response_data["flight_arrival_date"],
                flight_arrival_time=response_data["flight_arrival_time"],
                departure_airport=response_data["departure_airport"],
                arrival_airport=response_data["arrival_airport"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Weather


@router.get(
    "/weather",
    tags=["Weather"],
    status_code=200,
    description="Location weather",
    response_model=FiveDayWeather,
)
def location_weather(
    city: str,
    province: Optional[str] = None,
    country: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"{EXTERNAL_SERVICES_URL}/weather",
                params={"city": city, "province": province, "country": country},
            )

            handle_response_error(200, response)

            weather_data = response.json()

            return parse_weather_days(weather_data)

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Currency


@router.get(
    "/currency",
    tags=["Currency"],
    status_code=200,
    description="Currency conversion",
    response_model=Currency,
)
def currency_conversor(
    currency: str,
    interest_currency: str,
    amount: float,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"{EXTERNAL_SERVICES_URL}/currency",
                params={
                    "currency": currency,
                    "interest_currency": interest_currency,
                    "amount": amount,
                },
            )

            handle_response_error(200, response)

            currency_data = response.json()

            return Currency.model_construct(
                base_code=currency_data["base_code"],
                target_code=currency_data["target_code"],
                conversion=currency_data["conversion"],
            )
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


# Chatbot


@router.post(
    "/chatbot/init",
    tags=["Chatbot"],
    status_code=201,
    description="Start conversation",
)
async def init_conversation(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)
            response = requests.post(
                f"{EXTERNAL_SERVICES_URL}/chatbot/init",
                headers={"Authorization": f"Bearer {credentials.credentials}"},
                params={
                    "user_id": user_id,
                },
            )

            handle_response_error(201, response)

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.post(
    "/chatbot/send_message",
    tags=["Chatbot"],
    status_code=201,
    description="Send message to the assistant",
    response_model=AssistantResponse,
)
async def send_message(
    message: ChatMessage,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        if check_authentication(credentials):
            user_id = get_user_id(credentials)

            response = requests.post(
                f"{EXTERNAL_SERVICES_URL}/chatbot/send_message/{user_id}",
                json={"message": message.text},
            )

            handle_response_error(201, response)

            assistant_response = dict(response.json())

            return AssistantResponse.model_construct(
                role=assistant_response["role"],
                message=assistant_response["message"],
            )

    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


###########
#  Cities #
###########
@router.get(
    "/cities",
    tags=["Cities"],
    status_code=200,
    description="Get cities names",
    response_model=Cities,
)
async def get_cities_name(keyword: str):
    try:
        response = requests.get(
            f"{EXTERNAL_SERVICES_URL}/cities", params={"keyword": keyword}
        )

        handle_response_error(200, response)

        cities = response.json()

        return parse_cities(cities["cities"])
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
