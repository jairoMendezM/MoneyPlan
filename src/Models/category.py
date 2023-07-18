import uuid
from pydantic import BaseModel, Field

class Subcategory(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

class Category(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    subcategories: list[Subcategory.name] = []
    
    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True