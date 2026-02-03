from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
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

@router.post("/google")
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
                "role": request.role
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
        
        return {
            "message": "Authenticated",
            "user": map_document(user),
            "token": token,
            "role": user.get("role") # Original returns role from request or user? Original returns `role` variable which was from req.body
        }
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
