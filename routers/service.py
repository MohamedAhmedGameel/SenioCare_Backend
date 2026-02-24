from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.service import ServiceCreate, ServiceUpdate
from utils.pydantic_utils import map_document

router = APIRouter()


@router.post("/", status_code=201)
async def create_service(service: ServiceCreate):
    db = get_db()
    service_dict = service.model_dump(exclude_unset=True, by_alias=True)
    result = await db.services.insert_one(service_dict)
    created = await db.services.find_one({"_id": result.inserted_id})
    return map_document(created)


@router.get("/")
async def list_services():
    db = get_db()
    services = await db.services.find().to_list(length=None)
    return [map_document(s) for s in services]


@router.get("/{id}")
async def get_service(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    service = await db.services.find_one({"_id": ObjectId(id)})
    if not service:
        raise HTTPException(status_code=404, detail="Not found")

    return map_document(service)


@router.put("/{id}")
async def update_service(id: str, service: ServiceUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    existing = await db.services.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    updates = service.model_dump(exclude_unset=True, by_alias=True)
    if updates:
        await db.services.update_one({"_id": ObjectId(id)}, {"$set": updates})

    updated = await db.services.find_one({"_id": ObjectId(id)})
    return map_document(updated)


@router.delete("/{id}")
async def delete_service(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    result = await db.services.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}
