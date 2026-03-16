from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Any
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from config import GOOGLE_CLIENT_ID, JWT_SECRET
from database import get_db
from schemas.user import UserCreate, User
from utils.pydantic_utils import map_document

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    idToken: str
    role: str

from typing import Any, Dict, Optional

class AuthResponse(BaseModel):
    message: str
    user: User
    token: str
    role: str
    profile: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Authenticated",
                "user": {
                    "id": "65123...",
                    "googleId": "12345...",
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "avatar": "https://example.com/avatar.jpg",
                    "role": "elder",
                    "onBoard": True
                },
                "token": "eyJhbGciOi...",
                "role": "elder",
                "profile": {
                    "id": "65f12...",
                    "userId": "65123...",
                    "age": 70,
                    "gender": "male",
                    "chronicDiseases": ["Diabetes"],
                    "allergies": [],
                    "caregiver_ids": [],
                    "bloodType": "O+",
                    "mobilityStatus": "independent"
                }
            }
        }

@router.post("/google", response_model=AuthResponse)
async def google_auth(request: GoogleAuthRequest):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing GOOGLE_CLIENT_ID")
    if not JWT_SECRET:
         raise HTTPException(status_code=500, detail="Server misconfiguration: missing JWT_SECRET")
    
    try:
        # 1. Verify Google Token
        id_info = id_token.verify_oauth2_token(request.idToken, requests.Request(), GOOGLE_CLIENT_ID)
        
        # 2. Extract info
        sub = id_info['sub']
        email = id_info.get('email')
        name = id_info.get('name')
        picture = id_info.get('picture')
        
        db = get_db()
        users_collection = db["users"]
        
        # 3. Register or Login
        user = await users_collection.find_one({"googleId": sub})
        
        if not user:
            new_user = {
                "googleId": sub,
                "name": name,
                "email": email,
                "avatar": picture,
                "role": request.role,
                "onBoard": False
            }
            result = await users_collection.insert_one(new_user)
            user = await users_collection.find_one({"_id": result.inserted_id})
        
        # 4. Generate JWT
        # Original code used: { id: user._id, email: user.email, role: user.role }
        # Note: PyJWT encode returns a string in Python 3, but in old versions bytes.
        
        payload = {
            "id": str(user["_id"]),
            "email": email,
            "role": user.get("role")
        }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        
        profile = None
        if user.get("onBoard"):
            role_str = user.get("role")
            user_id_str = str(user["_id"])
            if role_str == "elder":
                profile_doc = await db.elders.find_one({"userId": user_id_str})
                if profile_doc:
                    profile = map_document(profile_doc)
            elif role_str == "caregiver":
                profile_doc = await db.caregivers.find_one({"userId": user_id_str})
                if profile_doc:
                    profile = map_document(profile_doc)
            elif role_str in ["serviceProvider"]:
                profile_doc = await db.serviceproviders.find_one({"userId": user_id_str})
                if profile_doc:
                    profile = map_document(profile_doc)
        
        return {
            "message": "Authenticated",
            "user": map_document(user),
            "token": token,
            "role": user.get("role"),
            "profile": profile
        }
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
