import uuid
from pydantic import BaseModel, Field

class Account(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    budget: str = Field(...)
    expenses: list[str] or None = None
    incomes: list[str] or None = None
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True