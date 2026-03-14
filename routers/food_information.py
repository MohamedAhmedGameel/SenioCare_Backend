from fastapi import APIRouter, HTTPException
from typing import List, Optional
from bson import ObjectId
from database import get_ai_db
from schemas.food_information import FoodInformationCreate, FoodInformationUpdate, FoodInformation, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201, response_model=FoodInformation)
async def create_food_information(food_info: FoodInformationCreate):
    """Create a new food information record"""
    db = get_ai_db()
    
    # Check if fhdi_food_id already exists
    existing = await db.food_information.find_one({"fhdi_food_id": food_info.fhdi_food_id})
    if existing:
        raise HTTPException(status_code=400, detail="Food with this fhdi_food_id already exists")
    
    food_dict = food_info.model_dump(exclude_unset=True)
    result = await db.food_information.insert_one(food_dict)
    created = await db.food_information.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/", response_model=List[FoodInformation])
async def list_food_information(
    food_name: Optional[str] = None,
    group: Optional[str] = None,
    subgroup: Optional[str] = None,
    page: int = 1,
    limit: int = 30
):
    """List all food information records with optional filters and pagination"""
    db = get_ai_db()
    
    skip = (page - 1) * limit
    
    # Build filter query
    query = {}
    if food_name:
        query["food_name"] = {"$regex": food_name, "$options": "i"}
    if group:
        query["group"] = group
    if subgroup:
        query["subgroup"] = subgroup
    
    foods = await db.food_information.find(query).skip(skip).limit(limit).to_list(length=None)
    
    for food in foods:
        map_document(food)
    
    return foods

@router.get("/fhdi/{fhdi_food_id}", response_model=FoodInformation)
async def get_food_by_fhdi_id(fhdi_food_id: str):
    """Get a specific food information record by fhdi_food_id"""
    db = get_ai_db()
    
    food = await db.food_information.find_one({"fhdi_food_id": fhdi_food_id})
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return map_document(food)

@router.get("/{id}", response_model=FoodInformation)
async def get_food_information(id: str):
    """Get a specific food information record by MongoDB ID"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    food = await db.food_information.find_one({"_id": ObjectId(id)})
    
    if not food:
        raise HTTPException(status_code=404, detail="Not found")
    
    return map_document(food)

@router.put("/{id}", response_model=FoodInformation)
async def update_food_information(id: str, food_info: FoodInformationUpdate):
    """Update a food information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    existing = await db.food_information.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    updates = food_info.model_dump(exclude_unset=True)
    
    if "fhdi_food_id" in updates:
        duplicate = await db.food_information.find_one({
            "fhdi_food_id": updates["fhdi_food_id"],
            "_id": {"$ne": ObjectId(id)}
        })
        if duplicate:
            raise HTTPException(status_code=400, detail="Another food with this fhdi_food_id already exists")
    
    if updates:
        await db.food_information.update_one({"_id": ObjectId(id)}, {"$set": updates})
    
    updated = await db.food_information.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}", response_model=DeleteResponse)
async def delete_food_information(id: str):
    """Delete a food information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    result = await db.food_information.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"message": "Deleted successfully"}
