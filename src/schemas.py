from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ----- User Schemas ---------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ----- Auth Schemas -----------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ----- Note Schemas ------------------------------------
class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    is_published: bool = False

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        from_attributes = True