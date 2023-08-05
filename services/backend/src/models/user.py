import uuid
from typing import Optional, Union
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Union[str, uuid.UUID] = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    user_name: str = Field(...)
    disabled: Optional[bool] = False

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True

class UserDB(User):
    password: str = Field(pattern=r'[A-Za-z0-9@#$%^&+=\-\_]{8,}')
