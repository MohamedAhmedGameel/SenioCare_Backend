from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from utils.pydantic_utils import PyObjectId

class UserBase(BaseModel):
    googleId: str
    name: str
    email: EmailStr
    avatar: Optional[str] = None
    role: str
    onBoard: bool = False

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {
            # custom encoders if needed
        }
