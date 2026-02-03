from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.elder import ElderCreate, ElderUpdate
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201)
async def create_elder(elder: ElderCreate):
    db = get_db()
    elder_dict = elder.model_dump(exclude_unset=True)
    result = await db.elders.insert_one(elder_dict)
    created = await db.elders.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_elders():
    db = get_db()
    pipeline = [
        {
            "$lookup": {
                "from": "caregivers",
                "localField": "caregiver_ids",
                "foreignField": "_id",
                "as": "caregiver_ids"
            }
        }
    ]
    elders = await db.elders.aggregate(pipeline).to_list(length=None)
    
    for e in elders:
        map_document(e)
        if "caregiver_ids" in e and isinstance(e["caregiver_ids"], list):
            for cg in e["caregiver_ids"]:
                map_document(cg)
    return elders

@router.get("/{id}")
async def get_elder(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    pipeline = [
        { "$match": { "_id": ObjectId(id) } },
        {
            "$lookup": {
                "from": "caregivers",
                "localField": "caregiver_ids",
                "foreignField": "_id",
                "as": "caregiver_ids"
            }
        }
    ]
    
    result = await db.elders.aggregate(pipeline).to_list(length=1)
    
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    elder = result[0]
    map_document(elder)
    if "caregiver_ids" in elder and isinstance(elder["caregiver_ids"], list):
        for cg in elder["caregiver_ids"]:
            map_document(cg)
            
    return elder

@router.put("/{id}")
async def update_elder(id: str, elder: ElderUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    existing = await db.elders.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
        
    updates = elder.model_dump(exclude_unset=True)
    if updates:
        await db.elders.update_one({"_id": ObjectId(id)}, {"$set": updates})
        
    updated = await db.elders.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}")
async def delete_elder(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    result = await db.elders.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {"message": "Deleted"}
