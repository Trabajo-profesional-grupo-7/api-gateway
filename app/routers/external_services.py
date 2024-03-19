from fastapi import FastAPI
from datetime import date
from app.schemas.external_services import *
import requests
from fastapi import APIRouter
from fastapi import status

router = APIRouter()

@router.get("/flights/status", tags=["Flights"])
async def flight_information(carrier_code: str, flight_number: str, departure_date: date):
    try:
        response = requests.get(
            f"http://external-services:8002/flights/status",
            params={
                "carrier_code": carrier_code,
                "flight_number": flight_number,
                "departure_date": departure_date,
            },
        )
        response.raise_for_status()  

        return response.json()
    except:
        return status(500)   