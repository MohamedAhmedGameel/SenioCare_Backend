from fastapi import APIRouter, HTTPException
from typing import Optional
from bson import ObjectId
from database import get_ai_db
from schemas.herb_information import HerbInformationCreate, HerbInformationUpdate
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201)
async def create_herb_information(herb_info: HerbInformationCreate):
    """Create a new herb information record"""
    db = get_ai_db()
    
    # Check if fhdi_herb_id already exists
    existing = await db.herb_information.find_one({"fhdi_herb_id": herb_info.fhdi_herb_id})
    if existing:
        raise HTTPException(status_code=400, detail="Herb with this fhdi_herb_id already exists")
    
    herb_dict = herb_info.model_dump(exclude_unset=True)
    result = await db.herb_information.insert_one(herb_dict)
    created = await db.herb_information.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_herb_information(
    herb_english_name: Optional[str] = None,
    therapeutic_class: Optional[str] = None,
    page: int = 1,
    limit: int = 30
):
    """List all herb information records with optional filters and pagination"""
    db = get_ai_db()
    
    skip = (page - 1) * limit
    
    # Build filter query
    query = {}
    if herb_english_name:
        query["herb_english_name"] = {"$regex": herb_english_name, "$options": "i"}  # Case-insensitive search
    if therapeutic_class:
        query["therapeutic_class"] = therapeutic_class
    
    herbs = await db.herb_information.find(query).skip(skip).limit(limit).to_list(length=None)
    
    for herb in herbs:
        map_document(herb)
    
    return herbs

@router.get("/fhdi/{fhdi_herb_id}")
async def get_herb_by_fhdi_id(fhdi_herb_id: str):
    """Get a specific herb information record by fhdi_herb_id"""
    db = get_ai_db()
    
    herb = await db.herb_information.find_one({"fhdi_herb_id": fhdi_herb_id})
    if not herb:
        raise HTTPException(status_code=404, detail="Herb not found")
    
    return map_document(herb)

@router.get("/{id}")
async def get_herb_information(id: str):
    """Get a specific herb information record by MongoDB ID"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    herb = await db.herb_information.find_one({"_id": ObjectId(id)})
    
    if not herb:
        raise HTTPException(status_code=404, detail="Not found")
    
    return map_document(herb)

@router.put("/{id}")
async def update_herb_information(id: str, herb_info: HerbInformationUpdate):
    """Update a herb information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    existing = await db.herb_information.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    updates = herb_info.model_dump(exclude_unset=True)
    
    # Check if updating fhdi_herb_id and if it already exists in another record
    if "fhdi_herb_id" in updates:
        duplicate = await db.herb_information.find_one({
            "fhdi_herb_id": updates["fhdi_herb_id"],
            "_id": {"$ne": ObjectId(id)}
        })
        if duplicate:
            raise HTTPException(status_code=400, detail="Another herb with this fhdi_herb_id already exists")
    
    if updates:
        await db.herb_information.update_one({"_id": ObjectId(id)}, {"$set": updates})
    
    updated = await db.herb_information.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}")
async def delete_herb_information(id: str):
    """Delete a herb information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    result = await db.herb_information.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"message": "Deleted successfully"}
