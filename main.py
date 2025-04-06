# Main application entry point
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from database import Base, engine

from routes import web, api

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# Add session middleware for web authentication
app.add_middleware(SessionMiddleware, secret_key="some_secret_key")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(web.router)
app.include_router(api.router, prefix="/api")