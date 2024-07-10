import unittest
from datetime import datetime
from unittest.mock import Mock

from pydantic import ValidationError

import app
from app.schemas.attractions_schemas.attractions import (
    Attraction,
    AttractionByID,
    AttractionByText,
    AttractionByUser,
    AttractionsFilter,
    AutocompleteAttractions,
    Comment,
    InteractiveAttraction,
    Location,
    ScheduleAttraction,
    SearchAttractionByText,
)


class TestAttractionsModels(unittest.TestCase):

    def test_location(self):
        location = Location(latitude=52.52, longitude=13.405)
        self.assertEqual(location.latitude, 52.52)
        self.assertEqual(location.longitude, 13.405)

        with self.assertRaises(ValidationError):
            Location(latitude="invalid", longitude=13.405)

    def test_attraction_by_id(self):
        location = Location(latitude=52.52, longitude=13.405)
        attraction = AttractionByID(
            id="1",
            displayName={"en": "Attraction"},
            likes_count=100,
            saved_count=50,
            done_count=30,
            avg_rating=4.5,
            location=location,
        )
        self.assertEqual(attraction.id, "1")
        self.assertEqual(attraction.displayName["en"], "Attraction")
        self.assertEqual(attraction.likes_count, 100)
        self.assertEqual(attraction.saved_count, 50)
        self.assertEqual(attraction.done_count, 30)
        self.assertEqual(attraction.avg_rating, 4.5)
        self.assertEqual(attraction.location, location)

    def test_schedule_attraction(self):
        scheduled_time = datetime.now()
        schedule = ScheduleAttraction(attraction_id="1", scheduled_time=scheduled_time)
        self.assertEqual(schedule.attraction_id, "1")
        self.assertEqual(schedule.scheduled_time, scheduled_time)

    def test_search_attraction_by_text(self):
        search = SearchAttractionByText(attraction_name="Obelisco")
        self.assertEqual(search.attraction_name, "Obelisco")

    def test_autocomplete_attractions(self):
        autocomplete = AutocompleteAttractions(attraction_name="Obelisco")
        self.assertEqual(autocomplete.attraction_name, "Obelisco")

    def test_comment(self):
        comment = Comment(comment_id=1, user_id=1, comment="Great place!")
        self.assertEqual(comment.comment_id, 1)
        self.assertEqual(comment.user_id, 1)
        self.assertEqual(comment.comment, "Great place!")

    def test_attractions_filter(self):
        filter = AttractionsFilter(attraction_types=["Museum", "Park"])
        self.assertEqual(filter.attraction_types, ["Museum", "Park"])

        filter = AttractionsFilter()
        self.assertIsNone(filter.attraction_types)

    def test_attraction_by_user(self):
        location = Location(latitude=52.52, longitude=13.405)
        comments = [Comment(comment_id=1, user_id=1, comment="Great place!")]
        attraction = AttractionByUser(
            attraction_id="1",
            attraction_name="Obelisco",
            location=location,
            city="Buenos Aires",
            country="Argentina",
            photo="photo_url",
            comments=comments,
            avg_rating=4.5,
            liked_count=100,
            is_liked=True,
            is_saved=True,
            user_rating=5,
            is_done=True,
            types=["Museum"],
            editorial_summary="A popular historical monument",
            google_maps_uri="https://maps.google.com/?q=obelisco",
            formatted_address="Av. 9 de Julio, Buenos Aires, Argentina",
        )

        self.assertEqual(attraction.attraction_id, "1")
        self.assertEqual(attraction.attraction_name, "Obelisco")
        self.assertEqual(attraction.location, location)
        self.assertEqual(attraction.city, "Buenos Aires")
        self.assertEqual(attraction.country, "Argentina")
        self.assertEqual(attraction.photo, "photo_url")
        self.assertEqual(attraction.comments, comments)
        self.assertEqual(attraction.avg_rating, 4.5)
        self.assertEqual(attraction.liked_count, 100)
        self.assertTrue(attraction.is_liked)
        self.assertTrue(attraction.is_saved)
        self.assertEqual(attraction.user_rating, 5)
        self.assertTrue(attraction.is_done)
        self.assertEqual(attraction.types, ["Museum"])
        self.assertEqual(attraction.editorial_summary, "A popular historical monument")
        self.assertEqual(
            attraction.google_maps_uri, "https://maps.google.com/?q=obelisco"
        )
        self.assertEqual(
            attraction.formatted_address, "Av. 9 de Julio, Buenos Aires, Argentina"
        )

    def test_interactive_attraction(self):
        interactive = InteractiveAttraction(
            user_id=1,
            attraction_id="1",
            attraction_name="Obelisco",
            attraction_country="Argentina",
            attraction_city="Buenos Aires",
        )
        self.assertEqual(interactive.user_id, 1)
        self.assertEqual(interactive.attraction_id, "1")
        self.assertEqual(interactive.attraction_name, "Obelisco")
        self.assertEqual(interactive.attraction_country, "Argentina")
        self.assertEqual(interactive.attraction_city, "Buenos Aires")
