import unittest

import app
from app.schemas.external_services_schemas.cities import Cities, City
from app.services.external_services.cities_services import parse_cities


class TestCitiesServices(unittest.TestCase):

    def test_parse_cities(self):
        cities_data = [
            {
                "name": "Buenos Aires",
                "country": "Argentina",
                "state_code": "AR",
                "latitude": 40.7128,
                "longitude": -74.0060,
            },
            {
                "name": "Cordoba",
                "country": "Argentina",
                "state_code": "AR",
                "latitude": 34.0522,
                "longitude": -118.2437,
            },
        ]

        cities = app.services.external_services.cities_services.parse_cities(
            cities_data
        )

        self.assertIsInstance(cities, Cities)
        self.assertEqual(len(cities.cities), 2)

        for idx, city in enumerate(cities.cities):
            self.assertIsInstance(city, City)
            self.assertEqual(city.name, cities_data[idx]["name"])
            self.assertEqual(city.country, cities_data[idx]["country"])
            self.assertEqual(city.state_code, cities_data[idx]["state_code"])
            self.assertEqual(city.latitude, cities_data[idx]["latitude"])
