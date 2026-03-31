from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from bson import ObjectId
from database import get_db
from schemas.daily_medicine import (
    DailyMedicineCreate, DailyMedicineUpdate, DailyMedicine,
    DailyMedicineSchedule, MedicineLogCreate, DeleteResponse,
)
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
        description="Date to check (YYYY-MM-DD). Defaults to today.",
    ),
):
    """
    Return all medicines for an elder that are active on the given date.
    Each time slot becomes a separate object with a combined 'date' field.
    State is pulled from the medicine_logs collection (defaults to 'pending').
    """
    db = get_db()

    if not target_date:
        target_date = date.today().isoformat()

    # Filter active medicines — treat missing end_date as ongoing
    query = {
        "elder_id": elder_id,
        "start_date": {"$lte": target_date},
        "$or": [
            {"end_date": {"$gte": target_date}},
            {"end_date": None},
            {"end_date": {"$exists": False}},
        ],
    }

    medicines = await db.daily_medicines.find(query).to_list(length=None)

    # Fetch all logs for this elder on this date
    logs = await db.medicine_logs.find({
        "elder_id": elder_id,
        "date": target_date,
    }).to_list(length=None)

    # Build a lookup: (medicine_id, time) -> state
    log_lookup = {}
    for log in logs:
        key = (str(log.get("medicine_id")), log.get("time"))
        log_lookup[key] = log.get("state", "pending")

    # Expand each medicine into one entry per time slot
    result = []
    for med in medicines:
        doc = map_document(med)
        med_id = str(doc.get("_id"))
        times_list = doc.get("times", []) or []
        for t in times_list:
            state = log_lookup.get((med_id, t), "pending")
            entry = {
                "_id": doc.get("_id"),
                "elder_id": doc.get("elder_id"),
                "medicine_name": doc.get("medicine_name"),
                "dosage": doc.get("dosage"),
                "medicine_type": doc.get("medicine_type"),
                "date": f"{target_date} {t}",
                "notes": doc.get("notes"),
                "state": state,
            }
            result.append(entry)

    # Sort chronologically by the date+time field
    result.sort(key=lambda x: x.get("date", ""))

    return result


# ── Medicine Log (per-day, per-time state tracking) ──────────────────────


@router.put("/{id}/log")
async def upsert_medicine_log(id: str, log: MedicineLogCreate):
    """
    Create or update a state log for a specific medicine + date + time.
    Example body: { "date": "2026-03-26", "time": "08:00", "state": "taken" }
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid medicine id")

    db = get_db()

    # Verify the medicine exists
    medicine = await db.daily_medicines.find_one({"_id": ObjectId(id)})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Upsert: one log per medicine + date + time
    filter_query = {
        "medicine_id": id,
        "elder_id": medicine.get("elder_id"),
        "date": log.date,
        "time": log.time,
    }
    update_doc = {
        "$set": {
            "state": log.state,
            "medicine_id": id,
            "elder_id": medicine.get("elder_id"),
            "date": log.date,
            "time": log.time,
        }
    }
    await db.medicine_logs.update_one(filter_query, update_doc, upsert=True)

    return {"message": f"Log updated: {log.state} for {log.date} {log.time}"}


# ── Standard CRUD (unchanged) ───────────────────────────────────────────


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
