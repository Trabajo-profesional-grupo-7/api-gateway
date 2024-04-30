from app.schemas.external_services_schemas.cities import Cities, City


def parse_cities(cities_data):
    all_cities = []

    for city in cities_data:
        city_instance = City(
            name=city["name"],
            country=city["country"],
            state_code=city["state_code"],
            latitude=city["latitude"],
            longitude=city["longitude"],
        )
        all_cities.append(city_instance)

    return Cities(cities=all_cities)
