from datetime import datetime

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
