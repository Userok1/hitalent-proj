from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pytest

from main import app
from src.database import get_session, Base


@pytest.fixture
def engine():
    db_url = "sqlite+pysqlite:///test.db"
    _engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )
    return _engine


@pytest.fixture
def session(engine):
    def get_session():
        return Session(engine)
    yield get_session
    

@pytest.fixture(autouse=True)
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="session")
def client():
    _client = TestClient(app=app)
    return _client


@pytest.fixture
def db_override(session):
    app.dependency_overrides[get_session] = session
    
    yield

    app.dependency_overrides.clear()