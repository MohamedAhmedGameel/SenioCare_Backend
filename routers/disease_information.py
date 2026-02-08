from fastapi import APIRouter, HTTPException
from typing import List, Optional
from bson import ObjectId
from database import get_ai_db
from schemas.disease_information import DiseaseInformationCreate, DiseaseInformationUpdate
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201)
async def create_disease_information(disease_info: DiseaseInformationCreate):
    """Create a new disease information record"""
    db = get_ai_db()
    disease_dict = disease_info.model_dump(exclude_unset=True)
    result = await db.disease_information.insert_one(disease_dict)
    created = await db.disease_information.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_disease_information(
    fhdi_drug_id: Optional[str] = None,
    indication: Optional[str] = None,
    page: int = 1,
    limit: int = 30
):
    """List all disease information records with optional filters and pagination"""
    db = get_ai_db()
    
    skip = (page - 1) * limit
    
    # Build filter query
    query = {}
    if fhdi_drug_id:
        query["fhdi_drug_id"] = fhdi_drug_id
    if indication:
        query["indication"] = {"$regex": indication, "$options": "i"}
    
    # Create aggregation pipeline with lookup for drug info
    pipeline = [
        {"$match": query} if query else {"$match": {}},
        # Lookup drug information
        {
            "$lookup": {
                "from": "drug_information",
                "localField": "fhdi_drug_id",
                "foreignField": "fhdi_drug_id",
                "as": "drug_details"
            }
        },
        {
            "$unwind": {
                "path": "$drug_details",
                "preserveNullAndEmptyArrays": True
            }
        },
        {"$skip": skip},
        {"$limit": limit}
    ]
    
    diseases = await db.disease_information.aggregate(pipeline).to_list(length=None)
    
    for disease in diseases:
        map_document(disease)
        if "drug_details" in disease and disease["drug_details"]:
            map_document(disease["drug_details"])
    
    return diseases

@router.get("/{id}")
async def get_disease_information(id: str):
    """Get a specific disease information record by ID"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {
            "$lookup": {
                "from": "drug_information",
                "localField": "fhdi_drug_id",
                "foreignField": "fhdi_drug_id",
                "as": "drug_details"
            }
        },
        {
            "$unwind": {
                "path": "$drug_details",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]
    
    result = await db.disease_information.aggregate(pipeline).to_list(length=1)
    
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    disease = result[0]
    map_document(disease)
    if "drug_details" in disease and disease["drug_details"]:
        map_document(disease["drug_details"])
    
    return disease

@router.put("/{id}")
async def update_disease_information(id: str, disease_info: DiseaseInformationUpdate):
    """Update a disease information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    existing = await db.disease_information.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    updates = disease_info.model_dump(exclude_unset=True)
    if updates:
        await db.disease_information.update_one({"_id": ObjectId(id)}, {"$set": updates})
    
    updated = await db.disease_information.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}")
async def delete_disease_information(id: str):
    """Delete a disease information record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    result = await db.disease_information.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"message": "Deleted successfully"}
