from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.elder import ElderCreate, ElderUpdate, ElderResponse, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()

async def _get_elder_with_caregivers(db, elder_id: ObjectId):
    """Fetch a single elder with its caregiver_ids populated as full objects."""
    pipeline = [
        { "$match": { "_id": elder_id } },
        {
            "$addFields": {
                "caregiver_ids": {
                    "$map": {
                        "input": { "$ifNull": ["$caregiver_ids", []] },
                        "as": "id",
                        "in": { "$toObjectId": "$$id" }
                    }
                }
            }
        },
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
        return None
    elder = result[0]
    map_document(elder)
    if "caregiver_ids" in elder and isinstance(elder["caregiver_ids"], list):
        for cg in elder["caregiver_ids"]:
            map_document(cg)
    return elder


@router.post("/", status_code=201, response_model=ElderResponse)
async def create_elder(elder: ElderCreate):
    db = get_db()
    elder_dict = elder.model_dump(exclude_unset=True)
    result = await db.elders.insert_one(elder_dict)
    # Mark the linked user as onBoarded
    if elder.userId:
        await db.users.update_one(
            {"_id": ObjectId(elder.userId)},
            {"$set": {"onBoard": True}}
        )
    return await _get_elder_with_caregivers(db, result.inserted_id)

@router.get("/", response_model=List[ElderResponse])
async def list_elders():
    db = get_db()

    pipeline = [
        {
            "$addFields": {
                "caregiver_ids": {
                    "$map": {
                        "input": { "$ifNull": ["$caregiver_ids", []] },
                        "as": "id",
                        "in": { "$toObjectId": "$$id" }
                    }
                }
            }
        },
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

@router.get("/{id}", response_model=ElderResponse)
async def get_elder(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    elder = await _get_elder_with_caregivers(db, ObjectId(id))
    if not elder:
        raise HTTPException(status_code=404, detail="Not found")
    return elder

@router.put("/{id}", response_model=ElderResponse)
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
        
    return await _get_elder_with_caregivers(db, ObjectId(id))

@router.delete("/{id}", response_model=DeleteResponse)
async def delete_elder(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    result = await db.elders.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {"message": "Deleted"}
