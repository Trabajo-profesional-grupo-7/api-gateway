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
        weather = Weather(
            humidity=int(weather_info.get("humidity", 0)),
            cloudCover=int(weather_info.get("cloudCover", 0)),
            precipitation_probability=int(
                weather_info.get("precipitation_probability", 0)
            ),
            temperature=weather_info.get("temperatureAvg", 0),
            uv_index=weather_info.get("uv_index", 0),
            visibility=weather_info.get("visibility", 0),
        )
        day_weather = DayWeather(date=datetime.fromisoformat(date_str), weather=weather)
        five_day_weather.append(day_weather)

    return FiveDayWeather(location=location, five_day_weather=five_day_weather)
