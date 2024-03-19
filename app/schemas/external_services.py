from pydantic import BaseModel

class Flight(BaseModel):
    carrier_code: str
    flight_number: str
    departure_date: str