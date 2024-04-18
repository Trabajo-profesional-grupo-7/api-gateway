from datetime import datetime
from typing import List

from pydantic import BaseModel


class AttractionByID(BaseModel):
    id: str
    displayName: dict
    likes_count: int
    saved_count: int
    done_count: int
    avg_rating: float


class AttractionByText(BaseModel):
    id: str
    adrFormatAddress: str
    displayName: dict
    likes_count: int
    saved_count: int
    done_count: int
    avg_rating: float


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


class AttractionByUser(BaseModel):
    attraction_id: str
    attraction_name: str
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


class Attraction(BaseModel):
    attraction_id: str
    attraction_name: str
    city: str = None
    country: str = None
    photo: str = None
