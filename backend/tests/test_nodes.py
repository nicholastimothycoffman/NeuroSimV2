def test_create_node(client, attention_payload):
    response = client.post("/nodes", json=attention_payload)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == attention_payload["name"]
    assert data["node_type"] == attention_payload["node_type"]
    assert data["description"] == attention_payload["description"]


def test_list_nodes(client, memory_payload):
    client.post("/nodes", json=memory_payload)

    response = client.get("/nodes")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_node(client):
    payload = {
        "name": "Anxiety",
        "node_type": "cognitive_state",
        "description": "Heightened threat sensitivity.",
    }

    created = client.post("/nodes", json=payload).json()

    response = client.get(f"/nodes/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]


def test_update_node(client):
    payload = {
        "name": "Focus",
        "node_type": "cognitive_state",
        "description": "Original description.",
    }

    created = client.post("/nodes", json=payload).json()

    response = client.put(
        f"/nodes/{created['id']}",
        json={"description": "Updated description."},
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Updated description."


def test_delete_node(client):
    payload = {
        "name": "Fatigue",
        "node_type": "factor",
        "description": "Reduced energy.",
    }

    created = client.post("/nodes", json=payload).json()

    response = client.delete(f"/nodes/{created['id']}")

    assert response.status_code == 204

    missing = client.get(f"/nodes/{created['id']}")
    assert missing.status_code == 404


def test_duplicate_node_name_returns_409(client, attention_payload):
    client.post("/nodes", json=attention_payload)
    response = client.post("/nodes", json=attention_payload)

    assert response.status_code == 409
