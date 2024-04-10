from datetime import date, datetime

from app.schemas.external_services_schemas.weather import (
    DayWeather,
    FiveDayWeather,
    Weather,
)


def parse_weather_days(weather_data: dict):
    location = weather_data.get("location")
    five_day_weather = []
    for item in weather_data.get("five_day_weather", []):
        date_str = item.get("date")
        weather_info = item.get("weather", {})
        weather = Weather(**weather_info)
        day_weather = DayWeather(date=datetime.fromisoformat(date_str), weather=weather)
        five_day_weather.append(day_weather)

    return FiveDayWeather(location=location, five_day_weather=five_day_weather)
