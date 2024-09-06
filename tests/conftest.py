import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from etl.config import load_config

# Load test configuration
config = load_config()

# Use the existing database for testing, but with a prefix for test tables
TEST_DB_URL = f"postgresql://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['db_name']}"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DB_URL)
    # Instead of creating all tables, we'll create them as needed in specific tests
    yield engine

@pytest.fixture(scope="function")
def test_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def test_client(test_session):
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="session")
def test_db_url():
    return TEST_DB_URL