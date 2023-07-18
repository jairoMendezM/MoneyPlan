import uuid
from pydantic import BaseModel, Field

class Budget(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    category: str = Field(...)
    budget: int = Field(...)
    period: int or None = None
    percentage_threshold: int = Field(...)
    
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True