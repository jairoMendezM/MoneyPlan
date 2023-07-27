import uuid
from ..util import period
from datetime import date
from pydantic import BaseModel, Field

class Saving(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    goal: int = Field(...)
    start_date: date = Field(...)
    end_date: date = Field(...)
    pay_day: int = Field(ge=1, le=28)
    available: int = 0
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True