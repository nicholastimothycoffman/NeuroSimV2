def test_create_relationship(client, attention_node, memory_node):
    payload = {
        "source_node_id": attention_node["id"],
        "target_node_id": memory_node["id"],
        "relationship_type": "supports",
        "description": "Attention supports working memory.",
        "weight": 0.9,
        "evidence_level": "strong",
    }

    response = client.post("/relationships", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["source_node_id"] == attention_node["id"]
    assert data["target_node_id"] == memory_node["id"]
    assert data["relationship_type"] == payload["relationship_type"]


def test_list_relationships(client, connected_graph):
    response = client.get("/relationships")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_relationship(client, connected_graph):
    relationship = connected_graph["relationship"]

    response = client.get(f"/relationships/{relationship['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == relationship["id"]


def test_delete_relationship(client, connected_graph):
    relationship = connected_graph["relationship"]

    response = client.delete(f"/relationships/{relationship['id']}")

    assert response.status_code == 204

    response = client.get(f"/relationships/{relationship['id']}")

    assert response.status_code == 404


def test_relationship_requires_existing_source(client, memory_node, relationship_payload):
    payload = {
        **relationship_payload,
        "source_node_id": 999,
        "target_node_id": memory_node["id"],
    }

    response = client.post("/relationships", json=payload)

    assert response.status_code == 404


def test_relationship_requires_existing_target(client, attention_node, relationship_payload):
    payload = {
        **relationship_payload,
        "source_node_id": attention_node["id"],
        "target_node_id": 999,
    }

    response = client.post("/relationships", json=payload)

    assert response.status_code == 404
