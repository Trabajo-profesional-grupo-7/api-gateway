import unittest

from pydantic import ValidationError

import app
from app.schemas.external_services_schemas.flights import Flight, FlightInfo


class TestFlightModels(unittest.TestCase):

    def test_flight(self):
        flight = Flight(
            carrier_code="AA", flight_number="100", departure_date="2023-07-05"
        )
        self.assertEqual(flight.carrier_code, "AA")
        self.assertEqual(flight.flight_number, "100")
        self.assertEqual(flight.departure_date, "2023-07-05")

    def test_flight_info(self):
        flight_info = FlightInfo(
            flight_departure_date="2023-07-05",
            flight_departure_time="14:30",
            flight_arrival_date="2023-07-05",
            flight_arrival_time="18:30",
            departure_airport="EZE",
            arrival_airport="MIA",
        )
        self.assertEqual(flight_info.flight_departure_date, "2023-07-05")
        self.assertEqual(flight_info.flight_departure_time, "14:30")
        self.assertEqual(flight_info.flight_arrival_date, "2023-07-05")
        self.assertEqual(flight_info.flight_arrival_time, "18:30")
        self.assertEqual(flight_info.departure_airport, "EZE")
        self.assertEqual(flight_info.arrival_airport, "MIA")
