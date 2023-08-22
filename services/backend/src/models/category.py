import uuid
from pydantic import BaseModel, Field

class Category(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    subcategories: list[str] = []
    type: bool = Field(description="Define if it is expense/income category")

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True