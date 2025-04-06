# Pydantic schemas for data validation and serialization
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

    class Config:
        orm_mode = True  # Enables conversion from SQLAlchemy models