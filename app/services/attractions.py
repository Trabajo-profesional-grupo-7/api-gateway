from app.schemas.attractions_schemas.attractions import (
    Attraction,
    AttractionByUser,
    Location,
)


def parse_attraction_by_id(data: dict):
    return AttractionByUser.model_construct(
        attraction_id=data["attraction_id"],
        attraction_name=data["attraction_name"],
        location=Location.model_construct(
            latitude=data["location"]["latitude"],
            longitude=data["location"]["longitude"],
        ),
        city=data["city"],
        country=data["country"],
        photo=data["photo"],
        comments=data["comments"],
        avg_rating=data["avg_rating"],
        liked_count=data["liked_count"],
        is_liked=data["is_liked"],
        is_saved=data["is_saved"],
        user_rating=data["user_rating"],
        is_done=data["is_done"],
    )


def parse_attraction_info(data: dict):
    return Attraction.model_construct(
        attraction_id=data["attraction_id"],
        attraction_name=data["attraction_name"],
        city=data["city"],
        location=Location.model_construct(
            latitude=data["location"]["latitude"],
            longitude=data["location"]["longitude"],
        ),
        country=data["country"],
        photo=data["photo"],
        avg_rating=data["avg_rating"],
        liked_count=data["liked_count"],
    )


def parse_attraction_list_info(attractions_list: list):
    attractions = []
    for attraction_data in attractions_list:
        attraction = parse_attraction_info(attraction_data)
        attractions.append(attraction)

    return attractions
