def test_create_node(client):
    response = client.post(
        "/nodes",
        json={
            "name": "Attention",
            "node_type": "cognitive_function",
            "description": "Selective cognitive focus.",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Attention"
    assert data["node_type"] == "cognitive_function"
    assert data["description"] == "Selective cognitive focus."


def test_list_nodes(client):
    client.post(
        "/nodes",
        json={
            "name": "Memory",
            "node_type": "cognitive_function",
            "description": "Information retention.",
        },
    )

    response = client.get("/nodes")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_node(client):
    created = client.post(
        "/nodes",
        json={
            "name": "Anxiety",
            "node_type": "cognitive_state",
            "description": "Heightened threat sensitivity.",
        },
    ).json()

    response = client.get(f"/nodes/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Anxiety"


def test_update_node(client):
    created = client.post(
        "/nodes",
        json={
            "name": "Focus",
            "node_type": "cognitive_state",
            "description": "Original description.",
        },
    ).json()

    response = client.put(
        f"/nodes/{created['id']}",
        json={"description": "Updated description."},
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Updated description."


def test_delete_node(client):
    created = client.post(
        "/nodes",
        json={
            "name": "Fatigue",
            "node_type": "factor",
            "description": "Reduced energy.",
        },
    ).json()

    response = client.delete(f"/nodes/{created['id']}")

    assert response.status_code == 204

    missing = client.get(f"/nodes/{created['id']}")
    assert missing.status_code == 404


def test_duplicate_node_name_returns_409(client):
    payload = {
        "name": "Attention",
        "node_type": "cognitive_function",
        "description": "Selective cognitive focus.",
    }

    client.post("/nodes", json=payload)
    response = client.post("/nodes", json=payload)

    assert response.status_code == 409
