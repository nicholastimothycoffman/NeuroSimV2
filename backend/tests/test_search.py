def test_search_nodes_by_name(client):
    client.post(
        "/nodes",
        json={
            "name": "Attention",
            "node_type": "cognitive_function",
            "description": "Selective focus.",
        },
    )

    response = client.get("/search/nodes?q=Attention")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Attention"


def test_search_nodes_by_description(client):
    client.post(
        "/nodes",
        json={
            "name": "Memory",
            "node_type": "cognitive_function",
            "description": "Information retention and recall.",
        },
    )

    response = client.get("/search/nodes?q=retention")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Memory"


def test_search_nodes_returns_empty_list_when_no_match(client):
    client.post(
        "/nodes",
        json={
            "name": "Anxiety",
            "node_type": "cognitive_state",
            "description": "Heightened threat sensitivity.",
        },
    )

    response = client.get("/search/nodes?q=nonexistent")

    assert response.status_code == 200
    assert response.json() == []


def test_search_nodes_requires_query(client):
    response = client.get("/search/nodes")

    assert response.status_code == 422
