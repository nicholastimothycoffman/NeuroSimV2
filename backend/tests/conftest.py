import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_neurosim.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def attention_payload():
    return {
        "name": "Attention",
        "node_type": "cognitive_function",
        "description": "Selective cognitive focus.",
    }


@pytest.fixture
def memory_payload():
    return {
        "name": "Memory",
        "node_type": "cognitive_function",
        "description": "Information retention.",
    }


@pytest.fixture
def relationship_payload():
    return {
        "relationship_type": "supports",
        "description": "Attention supports memory.",
        "weight": 1.0,
        "evidence_level": "moderate",
    }


@pytest.fixture
def attention_node(client, attention_payload):
    response = client.post("/nodes", json=attention_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def memory_node(client, memory_payload):
    response = client.post("/nodes", json=memory_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def connected_graph(client, attention_node, memory_node, relationship_payload):
    payload = {
        **relationship_payload,
        "source_node_id": attention_node["id"],
        "target_node_id": memory_node["id"],
    }

    response = client.post("/relationships", json=payload)
    assert response.status_code == 201

    return {
        "source": attention_node,
        "target": memory_node,
        "relationship": response.json(),
    }
