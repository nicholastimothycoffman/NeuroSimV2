def create_two_nodes(client):
    source = client.post(
        "/nodes",
        json={
            "name": "Attention",
            "node_type": "cognitive_function",
            "description": "Focus of cognition.",
        },
    ).json()

    target = client.post(
        "/nodes",
        json={
            "name": "Working Memory",
            "node_type": "cognitive_function",
            "description": "Temporary memory storage.",
        },
    ).json()

    return source, target


def test_create_relationship(client):
    source, target = create_two_nodes(client)

    response = client.post(
        "/relationships",
        json={
            "source_node_id": source["id"],
            "target_node_id": target["id"],
            "relationship_type": "supports",
            "description": "Attention supports working memory.",
            "weight": 0.9,
            "evidence_level": "strong",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["source_node_id"] == source["id"]
    assert data["target_node_id"] == target["id"]
    assert data["relationship_type"] == "supports"


def test_list_relationships(client):
    source, target = create_two_nodes(client)

    client.post(
        "/relationships",
        json={
            "source_node_id": source["id"],
            "target_node_id": target["id"],
            "relationship_type": "supports",
            "description": "",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    )

    response = client.get("/relationships")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_relationship(client):
    source, target = create_two_nodes(client)

    created = client.post(
        "/relationships",
        json={
            "source_node_id": source["id"],
            "target_node_id": target["id"],
            "relationship_type": "supports",
            "description": "",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    ).json()

    response = client.get(f"/relationships/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_delete_relationship(client):
    source, target = create_two_nodes(client)

    created = client.post(
        "/relationships",
        json={
            "source_node_id": source["id"],
            "target_node_id": target["id"],
            "relationship_type": "supports",
            "description": "",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    ).json()

    response = client.delete(f"/relationships/{created['id']}")

    assert response.status_code == 204

    response = client.get(f"/relationships/{created['id']}")

    assert response.status_code == 404


def test_relationship_requires_existing_source(client):
    _, target = create_two_nodes(client)

    response = client.post(
        "/relationships",
        json={
            "source_node_id": 999,
            "target_node_id": target["id"],
            "relationship_type": "supports",
            "description": "",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    )

    assert response.status_code == 404


def test_relationship_requires_existing_target(client):
    source, _ = create_two_nodes(client)

    response = client.post(
        "/relationships",
        json={
            "source_node_id": source["id"],
            "target_node_id": 999,
            "relationship_type": "supports",
            "description": "",
            "weight": 1.0,
            "evidence_level": "moderate",
        },
    )

    assert response.status_code == 404
