# Web routes for session-based authentication and task management
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Task
from auth import hash_password, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_web_user(request: Request, db: Session):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return db.query(User).filter(User.id == user_id).first()

@router.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already exists"})
    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "tasks": tasks})

@router.get("/tasks/add")
async def add_task_form(request: Request, db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("task_form.html", {"request": request, "action": "Add"})

@router.post("/tasks/add")
async def add_task(request: Request, title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    new_task = Task(title=title, description=description, user_id=user.id)
    db.add(new_task)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/tasks/edit/{id}")
async def edit_task_form(request: Request, id: int, db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    task = db.query(Task).filter(Task.id == id, Task.user_id == user.id).first()
    if task is None:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("task_form.html", {"request": request, "task": task, "action": "Edit"})

@router.post("/tasks/edit/{id}")
async def edit_task(request: Request, id: int, title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    task = db.query(Task).filter(Task.id == id, Task.user_id == user.id).first()
    if task is None:
        return RedirectResponse(url="/dashboard", status_code=303)
    task.title = title
    task.description = description
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/tasks/delete/{id}")
async def delete_task(request: Request, id: int, db: Session = Depends(get_db)):
    user = get_current_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    task = db.query(Task).filter(Task.id == id, Task.user_id == user.id).first()
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)