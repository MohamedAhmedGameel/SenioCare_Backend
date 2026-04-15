from pydantic import BaseModel
from typing import Any, Dict, Optional
from schemas.user import User


class UserWithProfile(BaseModel):
    user: User
    profile: Optional[Dict[str, Any]] = None
