import uuid
from typing import Optional, Union
from pydantic import BaseModel, Field
from datetime import date as Date
from pymongo import database as Database

class Expense(BaseModel):
    id: Union[str, uuid.UUID] = Field(default_factory=uuid.uuid4, alias='_id')
    category:  str = Field(...)
    subcategory: str = Field(...)
    bill: int = Field(...)
    date: Date = Field(...)
    pay_method: str = Field(...)
    description: Optional[str] = None
    user_name: str = Field(...)

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True
