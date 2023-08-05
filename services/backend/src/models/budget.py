import uuid
from pydantic import BaseModel, Field

class Budget(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    category: str = Field(description='Category Name')
    budget: int = Field(...)
    account: str = Field(description='Account Name')
    period: int or None = None
    percentage_threshold: int = Field(description='Threshold to alarm the user when its spending more money then it has to.')


    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True