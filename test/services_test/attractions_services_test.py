import unittest

import app
from app.schemas.attractions_schemas.attractions import AttractionByUser, Location
from app.services.attractions import *


class TestAttractionServices(unittest.TestCase):

    def test_parse_attraction_by_id(self):
        data = {
            "attraction_id": "1",
            "attraction_name": "Test Attraction",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "city": "Buenos Aires",
            "country": "Argentina",
            "photo": "attraction.jpg",
            "comments": [
                {"comment_id": 1, "user_id": 1, "comment": "Great place!"},
                {"comment_id": 2, "user_id": 2, "comment": "Fantastic!"},
            ],
            "avg_rating": 4.5,
            "liked_count": 100,
            "is_liked": True,
            "is_saved": False,
            "user_rating": 5,
            "is_done": True,
            "types": ["Museum", "Art"],
            "editorial_summary": "A great place to visit",
            "google_maps_uri": "https://maps.google.com",
            "formatted_address": "Santa fe 2990, Buenos Aires, Argentina",
        }

        attraction_by_user = parse_attraction_by_id(data)

        self.assertEqual(attraction_by_user.attraction_id, "1")
        self.assertEqual(attraction_by_user.attraction_name, "Test Attraction")
        self.assertEqual(attraction_by_user.location.latitude, 40.7128)
        self.assertEqual(attraction_by_user.location.longitude, -74.0060)
        self.assertEqual(attraction_by_user.city, "Buenos Aires")
        self.assertEqual(attraction_by_user.country, "Argentina")
        self.assertEqual(attraction_by_user.photo, "attraction.jpg")
        self.assertEqual(len(attraction_by_user.comments), 2)
        self.assertEqual(attraction_by_user.avg_rating, 4.5)
        self.assertEqual(attraction_by_user.liked_count, 100)
        self.assertTrue(attraction_by_user.is_liked)
        self.assertFalse(attraction_by_user.is_saved)
        self.assertEqual(attraction_by_user.user_rating, 5)
        self.assertTrue(attraction_by_user.is_done)
        self.assertEqual(attraction_by_user.types, ["Museum", "Art"])
        self.assertEqual(attraction_by_user.editorial_summary, "A great place to visit")
        self.assertEqual(attraction_by_user.google_maps_uri, "https://maps.google.com")
        self.assertEqual(
            attraction_by_user.formatted_address,
            "Santa fe 2990, Buenos Aires, Argentina",
        )

    def test_parse_attraction_info(self):
        data = {
            "attraction_id": "2",
            "attraction_name": "Test Attraction",
            "city": "Mendoza",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "country": "Argentina",
            "photo": "attraction.jpg",
            "avg_rating": 4.5,
            "liked_count": 100,
            "types": ["Museum", "Gallery"],
        }

        attraction = parse_attraction_info(data)

        self.assertIsInstance(attraction, Attraction)
        self.assertEqual(attraction.attraction_id, "2")
        self.assertEqual(attraction.attraction_name, "Test Attraction")
        self.assertEqual(attraction.city, "Mendoza")
        self.assertEqual(attraction.location.latitude, 40.7128)
        self.assertEqual(attraction.location.longitude, -74.0060)
        self.assertEqual(attraction.country, "Argentina")
        self.assertEqual(attraction.photo, "attraction.jpg")
        self.assertEqual(attraction.avg_rating, 4.5)
        self.assertEqual(attraction.liked_count, 100)
        self.assertEqual(attraction.types, ["Museum", "Gallery"])

    def test_parse_attraction_list_info(self):
        attractions_list = [
            {
                "attraction_id": "4",
                "attraction_name": "Test Attraction 1",
                "city": "Jujuy",
                "location": {"latitude": 42.7128, "longitude": -71.0060},
                "country": "Argentina",
                "photo": "attraction1.jpg",
                "avg_rating": 4.5,
                "liked_count": 100,
                "types": ["Cafe"],
            },
            {
                "attraction_id": "5",
                "attraction_name": "Test Attraction 2",
                "city": "Salta",
                "location": {"latitude": 31.0522, "longitude": -118.2437},
                "country": "Argentina",
                "photo": "attraction2.jpg",
                "avg_rating": 4.2,
                "liked_count": 80,
                "types": ["Park"],
            },
        ]

        attractions = parse_attraction_list_info(attractions_list)

        self.assertEqual(len(attractions), 2)
