from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class FoodInformationBase(BaseModel):
    fhdi_food_id: str
    food_name: str
    scientific_name: Optional[str] = None
    common_name: Optional[str] = None
    description: Optional[str] = None
    group: Optional[str] = None
    subgroup: Optional[str] = None
    drug_homologous_food: Optional[str] = None

class FoodInformationCreate(FoodInformationBase):
    pass

class FoodInformationUpdate(BaseModel):
    fhdi_food_id: Optional[str] = None
    food_name: Optional[str] = None
    scientific_name: Optional[str] = None
    common_name: Optional[str] = None
    description: Optional[str] = None
    group: Optional[str] = None
    subgroup: Optional[str] = None
    drug_homologous_food: Optional[str] = None

class FoodInformation(FoodInformationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {}
