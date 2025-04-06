# API routes for JWT-based authentication and task management
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Task
from schemas import UserLogin, TaskCreate, TaskUpdate, TaskResponse
from auth import verify_password, create_jwt_token, get_user_from_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_from_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/login")
async def api_login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(**task.dict(), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/tasks/{id}", response_model=TaskResponse)
async def update_task(id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{id}")
async def delete_task(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}