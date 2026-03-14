from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List, Literal
from utils.pydantic_utils import PyObjectId

class CaregiverBase(BaseModel):
    userId: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    relationship: Literal["son", "daughter", "nurse", "other"] = "other"
    elder_ids: List[PyObjectId] = []

class CaregiverCreate(CaregiverBase):
    pass

class CaregiverUpdate(BaseModel):
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    relationship: Optional[Literal["son", "daughter", "nurse", "other"]] = None
    elder_ids: Optional[List[PyObjectId]] = None

class Caregiver(CaregiverBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True


class CaregiverResponse(BaseModel):
    """Response schema for a caregiver with elder_ids populated as full objects."""
    id: Optional[str] = None
    _id: Optional[str] = None
    userId: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    relationship: Optional[str] = None
    elder_ids: List[Dict[str, Any]] = []

    class Config:
        populate_by_name = True
