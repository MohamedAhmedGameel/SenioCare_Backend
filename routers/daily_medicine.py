from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
from database import get_db
from schemas.daily_medicine import DailyMedicineCreate, DailyMedicineUpdate, DailyMedicine, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()


@router.post("/", status_code=201, response_model=DailyMedicine)
async def create_daily_medicine(medicine: DailyMedicineCreate):
    db = get_db()
    medicine_dict = medicine.model_dump(exclude_unset=True)
    result = await db.daily_medicines.insert_one(medicine_dict)
    created = await db.daily_medicines.find_one({"_id": result.inserted_id})
    return map_document(created)


@router.get("/", response_model=List[DailyMedicine])
async def list_daily_medicines():
    db = get_db()
    medicines = await db.daily_medicines.find().to_list(length=None)
    return [map_document(m) for m in medicines]


@router.get("/elder/{elder_id}", response_model=List[DailyMedicine])
async def get_daily_medicines_by_elder(
    elder_id: str,
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)")
):
    db = get_db()
    query = {"elder_id": elder_id}
    if date:
        query["date"] = date
        
    medicines = await db.daily_medicines.find(query).to_list(length=None)
    return [map_document(m) for m in medicines]


@router.get("/{id}", response_model=DailyMedicine)
async def get_daily_medicine(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    medicine = await db.daily_medicines.find_one({"_id": ObjectId(id)})
    if not medicine:
        raise HTTPException(status_code=404, detail="Not found")

    return map_document(medicine)


@router.put("/{id}", response_model=DailyMedicine)
async def update_daily_medicine(id: str, medicine: DailyMedicineUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    existing = await db.daily_medicines.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    updates = medicine.model_dump(exclude_unset=True)
    if updates:
        await db.daily_medicines.update_one({"_id": ObjectId(id)}, {"$set": updates})

    updated = await db.daily_medicines.find_one({"_id": ObjectId(id)})
    return map_document(updated)


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_daily_medicine(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")

    db = get_db()
    result = await db.daily_medicines.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}
