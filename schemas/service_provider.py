from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class ServiceProviderBase(BaseModel):
    userId: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    specialization: Optional[str] = None

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProviderUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    specialization: Optional[str] = None

class ServiceProvider(ServiceProviderBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
