from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import get_db
from schemas.medicine import MedicineCreate, MedicineUpdate, Medicine, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()


@router.post("/", status_code=201, response_model=Medicine)
async def create_medicine(medicine: MedicineCreate):
    db = get_db()
    medicine_dict = medicine.model_dump(exclude_unset=True)
    result = await db.medicines.insert_one(medicine_dict)
    created = await db.medicines.find_one({"_id": result.inserted_id})
    return map_document(created)


@router.get("/", response_model=List[Medicine])
async def list_medicines():
    db = get_db()
    medicines = await db.medicines.find().to_list(length=None)
    return [map_document(m) for m in medicines]


@router.get("/elder/{elder_id}", response_model=List[Medicine])
async def get_medicines_by_elder(elder_id: str):
    db = get_db()
    medicines = await db.medicines.find({"elder_id": elder_id}).to_list(length=None)
    return [map_document(m) for m in medicines]


@router.get("/{id}", response_model=Medicine)
async def get_medicine(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    medicine = await db.medicines.find_one({"_id": ObjectId(id)})
    if not medicine:
        raise HTTPException(status_code=404, detail="Not found")

    return map_document(medicine)


@router.put("/{id}", response_model=Medicine)
async def update_medicine(id: str, medicine: MedicineUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    existing = await db.medicines.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    updates = medicine.model_dump(exclude_unset=True)
    if updates:
        await db.medicines.update_one({"_id": ObjectId(id)}, {"$set": updates})

    updated = await db.medicines.find_one({"_id": ObjectId(id)})
    return map_document(updated)


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_medicine(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    result = await db.medicines.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}
