from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Any
from bson import ObjectId
from database import get_db
from schemas.caregiver import CaregiverCreate, CaregiverUpdate, Caregiver
from utils.pydantic_utils import map_document
import pymongo

router = APIRouter()

@router.post("/", status_code=201)
async def create_caregiver(caregiver: CaregiverCreate):
    db = get_db()
    # pickProvided logic is handled by Pydantic's exclude_unset=True usually,
    # but let's be explicit to match exact logic if needed.
    caregiver_dict = caregiver.model_dump(exclude_unset=True)
    
    # Convert str IDs to ObjectIds if present in input (Pydantic handles this mostly via PyObjectId validation)
    # But usually input JSON has strings.
    
    result = await db.caregivers.insert_one(caregiver_dict)
    created = await db.caregivers.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_caregivers():
    db = get_db()
    

    pipeline = [
        {
            "$addFields": {
                "elder_ids": {
                    "$map": {
                        "input": { "$ifNull": ["$elder_ids", []] },
                        "as": "id",
                        "in": { "$toObjectId": "$$id" }
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "elders",
                "localField": "elder_ids",
                "foreignField": "_id",
                "as": "elder_ids"
            }
        },
        # Mongoose populate returns the docs. We need to map _id to id for all of them?
        # The frontend might expect _id or id. Mongoose returns _id usually, unless transformed.
        # My map_document handles _id -> id and keeps _id.
    ]
    
    caregivers = await db.caregivers.aggregate(pipeline).to_list(length=None)
    
    # helper to map recursive structures if needed
    for c in caregivers:
        map_document(c)
        if "elder_ids" in c and isinstance(c["elder_ids"], list):
            for elder in c["elder_ids"]:
                map_document(elder)
                
    return caregivers

@router.get("/{id}")
async def get_caregiver(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()

    pipeline = [
        { "$match": { "_id": ObjectId(id) } },
        {
            "$addFields": {
                "elder_ids": {
                    "$map": {
                        "input": { "$ifNull": ["$elder_ids", []] },
                        "as": "id",
                        "in": { "$toObjectId": "$$id" }
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "elders",
                "localField": "elder_ids",
                "foreignField": "_id",
                "as": "elder_ids"
            }
        }
    ]

    
    result = await db.caregivers.aggregate(pipeline).to_list(length=1)
    
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    cg = result[0]
    print(cg)
    # map_document(cg)
    # if "elder_ids" in cg and isinstance(cg["elder_ids"], list):
    #     for elder in cg["elder_ids"]:
    #         map_document(elder)
            
    return cg

@router.put("/{id}")
async def update_caregiver(id: str, caregiver: CaregiverUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    
    # Check existence
    existing = await db.caregivers.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
        
    updates = caregiver.model_dump(exclude_unset=True)
    if updates:
        await db.caregivers.update_one({"_id": ObjectId(id)}, {"$set": updates})
        
    updated = await db.caregivers.find_one({"_id": ObjectId(id)})
    return map_document(updated) # Original updateCaregiver returns the updated doc (because it does findById, update props, save)

@router.delete("/{id}")
async def delete_caregiver(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    result = await db.caregivers.find_one_and_delete({"_id": ObjectId(id)})
    
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {"message": "Deleted"}
