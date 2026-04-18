from pydantic import BaseModel, Field
from typing import Optional, List
from utils.pydantic_utils import PyObjectId


class TimeSlot(BaseModel):
    from_time: str = Field(alias="from")
    to_time: str = Field(alias="to")

    class Config:
        populate_by_name = True


class AvailabilityDay(BaseModel):
    day: str
    timeSlots: List[TimeSlot] = []


class ServiceBase(BaseModel):
    service_provider_id: Optional[str] = None
    serviceDescription: Optional[str] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    availability: List[AvailabilityDay] = []
    isAvailable: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_provider_id: Optional[str] = None
    serviceDescription: Optional[str] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    availability: Optional[List[AvailabilityDay]] = None
    isAvailable: Optional[bool] = None


class Service(ServiceBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: Optional[str] = None

    class Config:
        populate_by_name = True


class DeleteResponse(BaseModel):
    message: str
