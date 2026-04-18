from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.service import ServiceCreate, ServiceUpdate, Service, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()


async def enrich_with_user_id(service_doc: dict) -> dict:
    """Look up the service provider and inject user_id into the service document."""
    mapped = map_document(service_doc)
    sp_id = mapped.get("service_provider_id")
    if sp_id and ObjectId.is_valid(sp_id):
        db = get_db()
        provider = await db.serviceproviders.find_one({"_id": ObjectId(sp_id)})
        if provider:
            mapped["user_id"] = provider.get("userId")
    return mapped


@router.post("/", status_code=201, response_model=Service)
async def create_service(service: ServiceCreate):
    db = get_db()
    service_dict = service.model_dump(exclude_unset=True, by_alias=True)
    result = await db.services.insert_one(service_dict)
    created = await db.services.find_one({"_id": result.inserted_id})
    return await enrich_with_user_id(created)


@router.get("/", response_model=List[Service])
async def list_services():
    db = get_db()
    services = await db.services.find().to_list(length=None)
    return [await enrich_with_user_id(s) for s in services]


@router.get("/provider/{service_provider_id}", response_model=List[Service])
async def get_services_by_provider(service_provider_id: str):
    db = get_db()
    services = await db.services.find({"service_provider_id": service_provider_id}).to_list(length=None)
    return [await enrich_with_user_id(s) for s in services]


@router.get("/{id}", response_model=Service)
async def get_service(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    service = await db.services.find_one({"_id": ObjectId(id)})
    if not service:
        raise HTTPException(status_code=404, detail="Not found")

    return await enrich_with_user_id(service)


@router.put("/{id}", response_model=Service)
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
    return await enrich_with_user_id(updated)


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_service(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    result = await db.services.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}
