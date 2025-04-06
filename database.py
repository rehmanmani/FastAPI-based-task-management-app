# Database configuration and session management
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskguard.db"

# Create engine with SQLite-specific arguments
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()