from fastapi import FastAPI
from datetime import date
from app.schemas.external_services import *
import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status
from app.utils.api_exception import *
from app.utils.constants import *
from app.services.autentication_service import check_authentication

router = APIRouter()
security = HTTPBearer()

@router.get("/flights/status", tags=["Flights"])
async def flight_information(carrier_code: str, flight_number: str, departure_date: date,credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if check_authentication(credentials):
            response = requests.get(
                f"http://external-services:8002/flights/status",
                params={
                    "carrier_code": carrier_code,
                    "flight_number": flight_number,
                    "departure_date": departure_date,
                },
            )
            
            if response.status_code == 404:
                raise APIException(code=FLIGTH_INFO_NOT_FOUND_ERROR, msg="FLIGTH_INFO_NOT_FOUND_ERROR")
        
            response_data = response.json()

            return FlightInfo.model_construct(
                flight_departure_date=response_data['flight_departure_date'],
                flight_departure_time=response_data['flight_departure_time'],
                flight_arrival_date=response_data['flight_arrival_date'],
                flight_arrival_time=response_data['flight_arrival_time'],
                departure_airport=response_data['departure_airport'],
                arrival_airport=response_data['arrival_airport'],
            )
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
