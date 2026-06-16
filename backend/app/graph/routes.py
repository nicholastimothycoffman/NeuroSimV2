from collections import deque

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.nodes.models import Node
from app.relationships.models import Relationship

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/neighbors/{node_id}")
def get_neighbors(node_id: int, db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    relationships = db.scalars(
        select(Relationship).where(
            or_(
                Relationship.source_node_id == node_id,
                Relationship.target_node_id == node_id,
            )
        )
    ).all()

    return {
        "node": {
            "id": node.id,
            "name": node.name,
            "node_type": node.node_type,
        },
        "neighbors": [
            {
                "relationship_id": rel.id,
                "relationship_type": rel.relationship_type,
                "direction": "outgoing" if rel.source_node_id == node_id else "incoming",
                "neighbor_node_id": rel.target_node_id if rel.source_node_id == node_id else rel.source_node_id,
            }
            for rel in relationships
        ],
    }


@router.get("/path")
def find_path(
    source_id: int = Query(...),
    target_id: int = Query(...),
    max_depth: int = Query(default=4, ge=1, le=10),
    db: Session = Depends(get_db),
):
    source = db.get(Node, source_id)
    target = db.get(Node, target_id)

    if not source:
        raise HTTPException(status_code=404, detail="Source node not found")

    if not target:
        raise HTTPException(status_code=404, detail="Target node not found")

    queue = deque([(source_id, [source_id])])
    visited = {source_id}

    while queue:
        current_id, path = queue.popleft()

        if len(path) > max_depth + 1:
            continue

        if current_id == target_id:
            nodes = db.scalars(select(Node).where(Node.id.in_(path))).all()
            node_map = {node.id: node for node in nodes}

            return {
                "source_id": source_id,
                "target_id": target_id,
                "path": [
                    {
                        "id": node_id,
                        "name": node_map[node_id].name,
                        "node_type": node_map[node_id].node_type,
                    }
                    for node_id in path
                ],
            }

        outgoing = db.scalars(
            select(Relationship).where(Relationship.source_node_id == current_id)
        ).all()

        for rel in outgoing:
            next_id = rel.target_node_id

            if next_id not in visited:
                visited.add(next_id)
                queue.append((next_id, path + [next_id]))

    return {
        "source_id": source_id,
        "target_id": target_id,
        "path": None,
        "message": "No path found within max_depth",
    }
