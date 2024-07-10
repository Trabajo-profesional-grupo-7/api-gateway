from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class AttractionByID(BaseModel):
    id: str
    displayName: dict
    likes_count: int
    saved_count: int
    done_count: int
    avg_rating: float
    location: Location


class AttractionByText(BaseModel):
    id: str
    adrFormatAddress: str
    displayName: dict
    location: Location
    saved_count: int
    done_count: int
    avg_rating: float
    liked_count: int


class ScheduleAttraction(BaseModel):
    attraction_id: str
    scheduled_time: datetime


class SearchAttractionByText(BaseModel):
    attraction_name: str


class AutocompleteAttractions(BaseModel):
    attraction_name: str


class Comment(BaseModel):
    comment_id: int
    user_id: int
    comment: str


class AttractionsFilter(BaseModel):
    attraction_types: Optional[List[str]] = None


class AttractionByUser(BaseModel):
    attraction_id: str
    attraction_name: str
    location: Location
    city: str = None
    country: str = None
    photo: str = None
    comments: List[Comment] = []
    avg_rating: float = None
    liked_count: int = 0
    is_liked: bool = False
    is_saved: bool = False
    user_rating: int = None
    is_done: bool = False
    types: List[str] = []
    editorial_summary: str
    google_maps_uri: str
    formatted_address: str


class Attraction(BaseModel):
    attraction_id: str
    attraction_name: str
    city: str = None
    country: str = None
    location: Location
    photo: str = None
    avg_rating: float
    liked_count: int
    types: List[str] = []


class InteractiveAttraction(BaseModel):
    user_id: int
    attraction_id: str
    attraction_name: str
    attraction_country: str
    attraction_city: str
