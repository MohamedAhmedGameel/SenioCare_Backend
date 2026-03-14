from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class DiseaseInformationBase(BaseModel):
    indication: Optional[str] = None
    state: Optional[str] = None
    fhdi_drug_id: str

class DiseaseInformationCreate(DiseaseInformationBase):
    pass

class DiseaseInformationUpdate(BaseModel):
    indication: Optional[str] = None
    state: Optional[str] = None
    fhdi_drug_id: Optional[str] = None

class DiseaseInformation(DiseaseInformationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {}


class DeleteResponse(BaseModel):
    message: str
