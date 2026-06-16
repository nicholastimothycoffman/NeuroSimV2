from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.nodes.models import Node
from app.relationships.models import Relationship
from app.relationships.schemas import RelationshipCreate, RelationshipRead

router = APIRouter(prefix="/relationships", tags=["relationships"])


@router.post("", response_model=RelationshipRead, status_code=status.HTTP_201_CREATED)
def create_relationship(payload: RelationshipCreate, db: Session = Depends(get_db)):
    source = db.get(Node, payload.source_node_id)
    target = db.get(Node, payload.target_node_id)

    if not source:
        raise HTTPException(status_code=404, detail="Source node not found")

    if not target:
        raise HTTPException(status_code=404, detail="Target node not found")

    relationship = Relationship(
        source_node_id=payload.source_node_id,
        target_node_id=payload.target_node_id,
        relationship_type=payload.relationship_type.value,
        description=payload.description,
        weight=payload.weight,
        evidence_level=payload.evidence_level,
    )

    db.add(relationship)
    db.commit()
    db.refresh(relationship)

    return relationship


@router.get("", response_model=list[RelationshipRead])
def list_relationships(db: Session = Depends(get_db)):
    return db.scalars(select(Relationship).order_by(Relationship.id)).all()


@router.get("/{relationship_id}", response_model=RelationshipRead)
def get_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship = db.get(Relationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")

    return relationship


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship = db.get(Relationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")

    db.delete(relationship)
    db.commit()

    return None
