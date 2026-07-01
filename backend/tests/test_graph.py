def create_connected_graph(client):
    attention = client.post(
        "/nodes",
        json={
            "name": "Attention",
            "node_type": "cognitive_function",
            "description": "Selective focus.",
        },
    ).json()

    memory = client.post(
        "/nodes",
        json={
            "name": "Memory",
            "node_type": "cognitive_function",
            "description": "Information retention.",
        },
    ).json()

    client.post(
        "/relationships",
        json={
            "source_node_id": attention["id"],
            "target_node_id": memory["id"],
            "relationship_type": "supports",
            "description": "Attention supports memory.",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    )

    return attention, memory


def test_get_neighbors(client):
    attention, memory = create_connected_graph(client)

    response = client.get(f"/graph/neighbors/{attention['id']}")

    assert response.status_code == 200

    data = response.json()
    assert data["node"]["id"] == attention["id"]
    assert len(data["neighbors"]) == 1
    assert data["neighbors"][0]["neighbor_node_id"] == memory["id"]
    assert data["neighbors"][0]["direction"] == "outgoing"


def test_get_neighbors_missing_node_returns_404(client):
    response = client.get("/graph/neighbors/999")

    assert response.status_code == 404


def test_find_path(client):
    attention, memory = create_connected_graph(client)

    response = client.get(
        f"/graph/path?source_id={attention['id']}&target_id={memory['id']}"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["source_id"] == attention["id"]
    assert data["target_id"] == memory["id"]
    assert len(data["path"]) == 2
    assert data["path"][0]["id"] == attention["id"]
    assert data["path"][1]["id"] == memory["id"]


def test_find_path_returns_none_when_no_path_exists(client):
    source = client.post(
        "/nodes",
        json={
            "name": "Anxiety",
            "node_type": "cognitive_state",
            "description": "Threat sensitivity.",
        },
    ).json()

    target = client.post(
        "/nodes",
        json={
            "name": "Sleep",
            "node_type": "factor",
            "description": "Restorative state.",
        },
    ).json()

    response = client.get(
        f"/graph/path?source_id={source['id']}&target_id={target['id']}"
    )

    assert response.status_code == 200
    assert response.json()["path"] is None


def test_find_path_missing_source_returns_404(client):
    target = client.post(
        "/nodes",
        json={
            "name": "Memory",
            "node_type": "cognitive_function",
            "description": "Information retention.",
        },
    ).json()

    response = client.get(f"/graph/path?source_id=999&target_id={target['id']}")

    assert response.status_code == 404


def test_find_path_missing_target_returns_404(client):
    source = client.post(
        "/nodes",
        json={
            "name": "Attention",
            "node_type": "cognitive_function",
            "description": "Selective focus.",
        },
    ).json()

    response = client.get(f"/graph/path?source_id={source['id']}&target_id=999")

    assert response.status_code == 404
