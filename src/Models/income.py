import uuid
from pydantic import BaseModel, Field
from datetime import date

class Income(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    category:  str = Field(...) # category id
    subcategory: str = Field(...)
    income: int = Field(...)
    account: str = Field(...) # account id
    date: date = Field(...)
    dote: str or None = None
    in_budget: bool or None = None
    in_total_account: bool or None
    user_name: str = Field(...) # user id
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True