from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from bson import ObjectId
from database import get_db
from schemas.daily_medicine import DailyMedicineCreate, DailyMedicineUpdate, DailyMedicine, DailyMedicineSchedule, DeleteResponse
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


@router.get("/elder/{elder_id}", response_model=List[DailyMedicineSchedule])
async def get_daily_medicines_by_elder(
    elder_id: str,
    target_date: Optional[str] = Query(
        None,
        alias="date",
        description="Date to check (YYYY-MM-DD). Defaults to today."
    )
):
    """
    Return all medicines for an elder that are active on the given date.
    Each time slot becomes a separate object with a 'date' field
    combining the query date and that time (e.g. "2026-03-26 08:00").
    Results are sorted chronologically by the date field.
    """
    db = get_db()

    if not target_date:
        target_date = date.today().isoformat()

    query = {
        "elder_id": elder_id,
        "start_date": {"$lte": target_date},
        "end_date": {"$gte": target_date},
    }

    medicines = await db.daily_medicines.find(query).to_list(length=None)

    # Expand each medicine into one entry per time slot
    result = []
    for med in medicines:
        doc = map_document(med)
        times_list = doc.get("times", []) or []
        for t in times_list:
            entry = {
                "_id": doc.get("_id"),
                "elder_id": doc.get("elder_id"),
                "medicine_name": doc.get("medicine_name"),
                "dosage": doc.get("dosage"),
                "medicine_type": doc.get("medicine_type"),
                "date": f"{target_date} {t}",
                "notes": doc.get("notes"),
                "state": doc.get("state"),
            }
            result.append(entry)

    # Sort by the date+time field
    result.sort(key=lambda x: x.get("date", ""))

    return result


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
