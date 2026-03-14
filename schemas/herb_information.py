from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class HerbInformationBase(BaseModel):
    fhdi_herb_id: str
    herb_latin_name: Optional[str] = None
    herb_english_name: Optional[str] = None
    herb_pinyin_name: Optional[str] = None
    herb_chinese_name: Optional[str] = None
    properties: Optional[str] = None
    function: Optional[str] = None
    indication: Optional[str] = None
    therapeutic_class: Optional[str] = None

class HerbInformationCreate(HerbInformationBase):
    pass

class HerbInformationUpdate(BaseModel):
    fhdi_herb_id: Optional[str] = None
    herb_latin_name: Optional[str] = None
    herb_english_name: Optional[str] = None
    herb_pinyin_name: Optional[str] = None
    herb_chinese_name: Optional[str] = None
    properties: Optional[str] = None
    function: Optional[str] = None
    indication: Optional[str] = None
    therapeutic_class: Optional[str] = None

class HerbInformation(HerbInformationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {}


class DeleteResponse(BaseModel):
    message: str
