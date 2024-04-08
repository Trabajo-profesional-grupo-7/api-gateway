from datetime import date, time

from pydantic import BaseModel


class Flight(BaseModel):
    carrier_code: str
    flight_number: str
    departure_date: str


class FlightInfo(BaseModel):
    flight_departure_date: str
    flight_departure_time: str
    flight_arrival_date: str
    flight_arrival_time: str
    departure_airport: str
    arrival_airport: str
