from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
from pathlib import Path

config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

DB_URL = f"postgresql://{config['rds']['username']}:{config['rds']['password']}@{config['rds']['host']}/{config['rds']['db_name']}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Generator function to create and manage database sessions.
    
    Yields:
        Session: A SQLAlchemy database session.
    
    Usage:
        This function is typically used with FastAPI's dependency injection system.
        It creates a new database session for each request and ensures the session
        is closed after the request is processed, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()