from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class DrugInformationBase(BaseModel):
    fhdi_drug_id: str
    drug_name: str
    synonyms: Optional[str] = None
    drug_type: Optional[str] = None
    summary: Optional[str] = None
    formula: Optional[str] = None

class DrugInformationCreate(DrugInformationBase):
    pass

class DrugInformationUpdate(BaseModel):
    fhdi_drug_id: Optional[str] = None
    drug_name: Optional[str] = None
    synonyms: Optional[str] = None
    drug_type: Optional[str] = None
    summary: Optional[str] = None
    formula: Optional[str] = None

class DrugInformation(DrugInformationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {}
