import uuid
from pydantic import BaseModel, Field
from datetime import date as Date

class Budget(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    category: str = Field(description='Category Name')
    budget: int = Field(...)
    balance: int = 0
    from_date: Date = Field(...)
    to_date: Date = Field(...)
    by_month: bool = True
    percentage_threshold: int = Field(description='Threshold to alarm the user when its spending more money then it has to.')

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True