import unittest
from datetime import date
from unittest.mock import Mock

from pydantic import ValidationError

import app
from app.schemas.external_services_schemas.weather import (
    DayWeather,
    FiveDayWeather,
    Weather,
)


class TestWeatherModels(unittest.TestCase):

    def test_weather(self):
        weather = Weather(
            humidity=85,
            cloudCover=70,
            precipitation_probability=40,
            temperature=22.5,
            uv_index=5,
            visibility=10.0,
        )
        self.assertEqual(weather.humidity, 85)
        self.assertEqual(weather.cloudCover, 70)
        self.assertEqual(weather.precipitation_probability, 40)
        self.assertEqual(weather.temperature, 22.5)
        self.assertEqual(weather.uv_index, 5)
        self.assertEqual(weather.visibility, 10.0)

    def test_day_weather(self):
        weather = Weather(
            humidity=85,
            cloudCover=70,
            precipitation_probability=40,
            temperature=22.5,
            uv_index=5,
            visibility=10.0,
        )
        day_weather = DayWeather(date=date(2023, 7, 5), weather=weather)
        self.assertEqual(day_weather.date, date(2023, 7, 5))
        self.assertEqual(day_weather.weather, weather)

    def test_five_day_weather(self):
        weather = Weather(
            humidity=85,
            cloudCover=70,
            precipitation_probability=40,
            temperature=22.5,
            uv_index=5,
            visibility=10.0,
        )
        day_weather = DayWeather(date=date(2023, 7, 5), weather=weather)
        five_day_weather = FiveDayWeather(
            location="Cordoba",
            five_day_weather=[
                day_weather,
                day_weather,
                day_weather,
                day_weather,
                day_weather,
            ],
        )
        self.assertEqual(five_day_weather.location, "Cordoba")
        self.assertEqual(len(five_day_weather.five_day_weather), 5)
        for day in five_day_weather.five_day_weather:
            self.assertEqual(day, day_weather)
