import uuid
from pydantic import BaseModel, Field
from datetime import date

class Expense(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    category:  str = Field(...)
    subcategory: str = Field(...)
    bill: int = Field(...)
    account: str = Field(...)
    date: date = Field(...)
    note: str or None = None
    in_budget: bool or None = None
    in_total_account: bool or None
    user_name: str = Field(...)
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True