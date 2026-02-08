from fastapi import APIRouter, HTTPException
from typing import Optional
from bson import ObjectId
from database import get_ai_db
from schemas.drug_information import DrugInformationCreate, DrugInformationUpdate
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201)
async def create_drug_information(drug_info: DrugInformationCreate):
    """Create a new drug information record"""
    db = get_ai_db()
    
    # Check if fhdi_drug_id already exists
    existing = await db.drug_information.find_one({"fhdi_drug_id": drug_info.fhdi_drug_id})
    if existing:
        raise HTTPException(status_code=400, detail="Drug with this fhdi_drug_id already exists")
    
    drug_dict = drug_info.model_dump(exclude_unset=True)
    result = await db.drug_information.insert_one(drug_dict)
    created = await db.drug_information.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_drug_information(
    drug_name: Optional[str] = None,
    drug_type: Optional[str] = None,
    page: int = 1,
    limit: int = 30
):
    """List all drug information records with optional filters and pagination"""
    db = get_ai_db()
    
    skip = (page - 1) * limit
    
    # Build filter query
    query = {}
    if drug_name:
        query["drug_name"] = {"$regex": drug_name, "$options": "i"}  # Case-insensitive search
    if drug_type:
        query["drug_type"] = drug_type
    
    drugs = await db.drug_information.find(query).skip(skip).limit(limit).to_list(length=None)
    
    for drug in drugs:
        map_document(drug)
    
    return drugs

@router.get("/fhdi/{fhdi_drug_id}")
async def get_drug_by_fhdi_id(fhdi_drug_id: str):
    """Get a specific drug information record by fhdi_drug_id"""
    db = get_ai_db()
    
    drug = await db.drug_information.find_one({"fhdi_drug_id": fhdi_drug_id})
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    return map_document(drug)

@router.get("/{id}")
async def get_drug_information(id: str):
    """Get a specific drug information record by MongoDB ID"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    drug = await db.drug_information.find_one({"_id": ObjectId(id)})
    
    if not drug:
        raise HTTPException(status_code=404, detail="Not found")
    
    return map_document(drug)

@router.put("/{id}")
async def update_drug_information(id: str, drug_info: DrugInformationUpdate):
    """Update a drug information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    existing = await db.drug_information.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    updates = drug_info.model_dump(exclude_unset=True)
    
    # Check if updating fhdi_drug_id and if it already exists in another record
    if "fhdi_drug_id" in updates:
        duplicate = await db.drug_information.find_one({
            "fhdi_drug_id": updates["fhdi_drug_id"],
            "_id": {"$ne": ObjectId(id)}
        })
        if duplicate:
            raise HTTPException(status_code=400, detail="Another drug with this fhdi_drug_id already exists")
    
    if updates:
        await db.drug_information.update_one({"_id": ObjectId(id)}, {"$set": updates})
    
    updated = await db.drug_information.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}")
async def delete_drug_information(id: str):
    """Delete a drug information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    result = await db.drug_information.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"message": "Deleted successfully"}
