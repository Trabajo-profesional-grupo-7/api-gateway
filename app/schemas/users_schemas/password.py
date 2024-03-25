from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str = Field("password", min_length=8)
