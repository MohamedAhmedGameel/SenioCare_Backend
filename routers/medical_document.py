from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.medical_document import MedicalDocumentCreate, MedicalDocumentUpdate, MedicalDocument, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()


@router.post("/", status_code=201, response_model=MedicalDocument)
async def create_medical_document(document: MedicalDocumentCreate):
    db = get_db()
    document_dict = document.model_dump(exclude_unset=True)
    result = await db.medical_documents.insert_one(document_dict)
    created = await db.medical_documents.find_one({"_id": result.inserted_id})
    return map_document(created)


@router.get("/", response_model=List[MedicalDocument])
async def list_medical_documents():
    db = get_db()
    documents = await db.medical_documents.find().to_list(length=None)
    return [map_document(d) for d in documents]


@router.get("/elder/{elder_id}", response_model=List[MedicalDocument])
async def get_documents_by_elder(elder_id: str):
    db = get_db()
    documents = await db.medical_documents.find({"elder_id": elder_id}).to_list(length=None)
    return [map_document(d) for d in documents]


@router.get("/{id}", response_model=MedicalDocument)
async def get_medical_document(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    document = await db.medical_documents.find_one({"_id": ObjectId(id)})
    if not document:
        raise HTTPException(status_code=404, detail="Not found")

    return map_document(document)


@router.put("/{id}", response_model=MedicalDocument)
async def update_medical_document(id: str, document: MedicalDocumentUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    existing = await db.medical_documents.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    updates = document.model_dump(exclude_unset=True)
    if updates:
        await db.medical_documents.update_one({"_id": ObjectId(id)}, {"$set": updates})

    updated = await db.medical_documents.find_one({"_id": ObjectId(id)})
    return map_document(updated)


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_medical_document(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    result = await db.medical_documents.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}
