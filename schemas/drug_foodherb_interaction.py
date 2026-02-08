from pydantic import BaseModel, Field
from typing import Optional
from utils.pydantic_utils import PyObjectId

class DrugFoodHerbInteractionBase(BaseModel):
    fhdi_drug_id: str
    drug_name: str
    drug_dose: Optional[str] = None
    dosage_form: Optional[str] = None
    food_herb_id: str
    food_herb_name: str
    type: str  # food or herb
    component: Optional[str] = None
    dose: Optional[str] = None
    time: Optional[str] = None
    effect: Optional[str] = None
    conclusion: Optional[str] = None

class DrugFoodHerbInteractionCreate(DrugFoodHerbInteractionBase):
    pass

class DrugFoodHerbInteractionUpdate(BaseModel):
    fhdi_drug_id: Optional[str] = None
    drug_name: Optional[str] = None
    drug_dose: Optional[str] = None
    dosage_form: Optional[str] = None
    food_herb_id: Optional[str] = None
    food_herb_name: Optional[str] = None
    type: Optional[str] = None
    component: Optional[str] = None
    dose: Optional[str] = None
    time: Optional[str] = None
    effect: Optional[str] = None
    conclusion: Optional[str] = None

class DrugFoodHerbInteraction(DrugFoodHerbInteractionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        json_encoders = {}
