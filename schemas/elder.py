from pydantic import BaseModel, Field
from typing import Optional, List
from utils.pydantic_utils import PyObjectId

class ElderBase(BaseModel):
    userId: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None
    chronicDiseases: List[str] = []
    allergies: List[str] = []
    caregiver_ids: List[PyObjectId] = []
    bloodType: Optional[str] = None
    mobilityStatus: Optional[str] = None

class ElderCreate(ElderBase):
    pass

class ElderUpdate(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None
    chronicDiseases: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    caregiver_ids: Optional[List[PyObjectId]] = None
    bloodType: Optional[str] = None
    mobilityStatus: Optional[str] = None

class Elder(ElderBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
