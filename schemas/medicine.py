from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId


class MedicineBase(BaseModel):
    elder_id: Optional[str] = None
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    medicine_type: Optional[str] = None
    notes: Optional[str] = None


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    elder_id: Optional[str] = None
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    medicine_type: Optional[str] = None
    notes: Optional[str] = None


class Medicine(MedicineBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True


class DeleteResponse(BaseModel):
    message: str
