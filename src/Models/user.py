import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_name: str

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    user_name: str = Field(...)
    disabled: Optional[bool] = False

    class Config:
        populate_by_name = True
        validate_assignment=True
        hide_input_in_errors=True

class UserDB(User):
    password: str = Field(...)

