import uuid
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import database as Database

class Account(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    total: int = Field(...)
    user_name: str = Field(...)

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True

