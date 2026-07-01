def test_search_nodes_by_name(client, attention_node):
    response = client.get("/search/nodes?q=Attention")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == attention_node["name"]


def test_search_nodes_by_description(client, memory_node):
    response = client.get("/search/nodes?q=retention")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == memory_node["name"]


def test_search_nodes_returns_empty_list_when_no_match(client):
    payload = {
        "name": "Anxiety",
        "node_type": "cognitive_state",
        "description": "Heightened threat sensitivity.",
    }

    client.post("/nodes", json=payload)

    response = client.get("/search/nodes?q=nonexistent")

    assert response.status_code == 200
    assert response.json() == []


def test_search_nodes_requires_query(client):
    response = client.get("/search/nodes")

    assert response.status_code == 422
