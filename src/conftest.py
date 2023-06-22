from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from leaf.config import Base
from leaf.dependencies import get_db
from leaf.main import app
from tests.factories.common import FactoriesSession
from tests.test_database import SQLALCHEMY_TESTING_DATABASE_URL, engine


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    if not database_exists(SQLALCHEMY_TESTING_DATABASE_URL):
        create_database(engine.url)
    with engine.connect() as connection:
        create_extension = text(
            f"CREATE EXTENSION IF NOT EXISTS postgis;",
        )
        connection.execute(create_extension)
    Base.metadata.create_all(bind=engine)

    yield engine

    drop_database(engine.url)


@pytest.fixture(scope="session")
def db(db_engine):
    connection = db_engine.connect()
    db = Session(bind=connection)

    yield db

    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def factory_boy_session(db_engine):
    FactoriesSession.bind = db_engine
