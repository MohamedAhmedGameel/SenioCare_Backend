from pydantic import BaseModel, Field
from typing import Optional, List
from utils.pydantic_utils import PyObjectId


class MedicalDocumentBase(BaseModel):
    document_name: Optional[str] = None
    date: Optional[str] = None
    images: List[str] = []


class MedicalDocumentCreate(MedicalDocumentBase):
    pass


class MedicalDocumentUpdate(BaseModel):
    document_name: Optional[str] = None
    date: Optional[str] = None
    images: Optional[List[str]] = None


class MedicalDocument(MedicalDocumentBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
