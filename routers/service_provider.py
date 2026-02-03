from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.service_provider import ServiceProviderCreate, ServiceProviderUpdate
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201)
async def create_service_provider(provider: ServiceProviderCreate):
    db = get_db()
    provider_dict = provider.model_dump(exclude_unset=True)
    result = await db.serviceproviders.insert_one(provider_dict)
    created = await db.serviceproviders.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/")
async def list_service_providers():
    db = get_db()
    providers = await db.serviceproviders.find().to_list(length=None)
    return [map_document(p) for p in providers]

@router.get("/{id}")
async def get_service_provider(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    provider = await db.serviceproviders.find_one({"_id": ObjectId(id)})
    if not provider:
        raise HTTPException(status_code=404, detail="Not found")
        
    return map_document(provider)

@router.put("/{id}")
async def update_service_provider(id: str, provider: ServiceProviderUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    existing = await db.serviceproviders.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
        
    updates = provider.model_dump(exclude_unset=True)
    if updates:
        await db.serviceproviders.update_one({"_id": ObjectId(id)}, {"$set": updates})
        
    updated = await db.serviceproviders.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}")
async def delete_service_provider(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
        
    db = get_db()
    result = await db.serviceproviders.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {"message": "Deleted"}
