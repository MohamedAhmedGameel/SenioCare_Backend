from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import get_db
from schemas.user_profile import UserWithProfile
from utils.pydantic_utils import map_document

router = APIRouter()


@router.get("/{user_id}", response_model=UserWithProfile)
async def get_user_with_profile(user_id: str):
    """Get user data along with their role-specific profile.

    Looks up the user by _id, then based on the user's role field,
    queries the matching role collection (elders, caregivers, serviceproviders)
    using userId as the foreign key.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = None
    role = user.get("role")
    uid = str(user["_id"])

    if role == "elder":
        profile = await db.elders.find_one({"userId": uid})
    elif role == "caregiver":
        profile = await db.caregivers.find_one({"userId": uid})
    elif role == "serviceProvider":
        profile = await db.serviceproviders.find_one({"userId": uid})

    return {
        "user": map_document(user),
        "profile": map_document(profile) if profile else None,
    }
