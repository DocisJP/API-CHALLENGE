import os
from pathlib import Path
import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    try:
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

config = load_config()

# Determine environment
IS_DOCKER = os.environ.get('DOCKER_CONTAINER', 'false').lower() == 'true'
IS_AWS = 'AWS_EXECUTION_ENV' in os.environ
IS_LOCAL = not (IS_DOCKER or IS_AWS)

logger.info(f"Running in {'Docker' if IS_DOCKER else 'AWS' if IS_AWS else 'local'} environment")

# Construct database URL
def get_database_url():
    if IS_DOCKER:
        db_config = {
            'host': 'db',
            'port': 5432,
            'db_name': config['local_db']['db_name'],
            'username': config['local_db']['username'],
            'password': config['local_db']['password']
        }
    elif IS_AWS:
        db_config = config['rds']
    else:
        db_config = config['local_db']
    
    return f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

DB_URL = get_database_url()
logger.info(f"Database URL constructed: {DB_URL.replace(config['local_db']['password'], '****')}")

# Create SQLAlchemy engine
try:
    engine = create_engine(DB_URL, echo=True)  # Set echo=True for SQL query logging
    logger.info("SQLAlchemy engine created successfully")
except Exception as e:
    logger.error(f"Failed to create SQLAlchemy engine: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error occurred during database session: {str(e)}")
        raise
    finally:
        db.close()

# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            logger.info("Successfully connected to the database")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection()