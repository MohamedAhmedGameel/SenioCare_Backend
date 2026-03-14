from pydantic import BaseModel, Field
from typing import Optional, List, Literal
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
    
    # For population, we might want a separate schema or nested model, 
    # but for now we keep the structure generic to allow either ID or object if populated manually
    # However, strictly typing it as List[Any] or List[Elder] is complex with circular deps.
    # We will handle population in the router response construction.

    class Config:
        populate_by_name = True
