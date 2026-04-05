from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str]=None
    email: Optional[str]=None
    age: Optional[int]=None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes=True
