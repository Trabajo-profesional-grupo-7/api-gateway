import unittest
from datetime import datetime

import app
from app.schemas.external_services_schemas.weather import (
    DayWeather,
    FiveDayWeather,
    Weather,
)
from app.services.external_services.weather_services import parse_weather_days


class TestParseWeatherDays(unittest.TestCase):

    def test_parse_weather_days(self):
        weather_data = {
            "location": "CABA",
            "five_day_weather": [
                {
                    "date": "2024-07-05",
                    "weather": {
                        "humidity": 70,
                        "cloudCover": 50,
                        "precipitation_probability": 20,
                        "temperature": 25.5,
                        "uv_index": 7,
                        "visibility": 10.0,
                    },
                },
                {
                    "date": "2024-07-06",
                    "weather": {
                        "humidity": 65,
                        "cloudCover": 40,
                        "precipitation_probability": 15,
                        "temperature": 26.0,
                        "uv_index": 8,
                        "visibility": 9.5,
                    },
                },
                {
                    "date": "2024-07-07",
                    "weather": {
                        "humidity": 70,
                        "cloudCover": 50,
                        "precipitation_probability": 20,
                        "temperature": 25.5,
                        "uv_index": 7,
                        "visibility": 10.0,
                    },
                },
                {
                    "date": "2024-07-08",
                    "weather": {
                        "humidity": 70,
                        "cloudCover": 50,
                        "precipitation_probability": 20,
                        "temperature": 25.5,
                        "uv_index": 7,
                        "visibility": 10.0,
                    },
                },
                {
                    "date": "2024-07-09",
                    "weather": {
                        "humidity": 70,
                        "cloudCover": 50,
                        "precipitation_probability": 20,
                        "temperature": 25.5,
                        "uv_index": 7,
                        "visibility": 10.0,
                    },
                },
            ],
        }

        five_day_weather_obj = (
            app.services.external_services.weather_services.parse_weather_days(
                weather_data
            )
        )

        self.assertIsInstance(five_day_weather_obj, FiveDayWeather)
        self.assertEqual(five_day_weather_obj.location, "CABA")
        self.assertEqual(len(five_day_weather_obj.five_day_weather), 5)

        for idx, day_weather in enumerate(five_day_weather_obj.five_day_weather):
            self.assertIsInstance(day_weather, DayWeather)
            self.assertEqual(
                day_weather.date,
                datetime.fromisoformat(
                    weather_data["five_day_weather"][idx]["date"]
                ).date(),
            )
            self.assertEqual(
                day_weather.weather.humidity,
                weather_data["five_day_weather"][idx]["weather"]["humidity"],
            )
            self.assertEqual(
                day_weather.weather.cloudCover,
                weather_data["five_day_weather"][idx]["weather"]["cloudCover"],
            )
            self.assertEqual(
                day_weather.weather.precipitation_probability,
                weather_data["five_day_weather"][idx]["weather"][
                    "precipitation_probability"
                ],
            )
            self.assertEqual(
                day_weather.weather.temperature,
                weather_data["five_day_weather"][idx]["weather"]["temperature"],
            )
            self.assertEqual(
                day_weather.weather.uv_index,
                weather_data["five_day_weather"][idx]["weather"]["uv_index"],
            )
            self.assertEqual(
                day_weather.weather.visibility,
                weather_data["five_day_weather"][idx]["weather"]["visibility"],
            )
