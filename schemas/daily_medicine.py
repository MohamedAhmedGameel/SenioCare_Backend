from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId


class DailyMedicineBase(BaseModel):
    elder_id: Optional[str] = None
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    medicine_type: Optional[str] = None
    times: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None
    state: Optional[str] = None


class DailyMedicineCreate(DailyMedicineBase):
    pass


class DailyMedicineUpdate(BaseModel):
    elder_id: Optional[str] = None
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    medicine_type: Optional[str] = None
    times: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None
    state: Optional[str] = None


class DailyMedicine(DailyMedicineBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True


class DeleteResponse(BaseModel):
    message: str
