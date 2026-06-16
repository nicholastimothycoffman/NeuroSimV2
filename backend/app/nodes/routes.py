from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.nodes.models import Node
from app.nodes.schemas import NodeCreate, NodeRead, NodeUpdate

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("", response_model=NodeRead, status_code=status.HTTP_201_CREATED)
def create_node(payload: NodeCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Node).where(Node.name == payload.name))
    if existing:
        raise HTTPException(status_code=409, detail="Node name already exists")

    node = Node(
        name=payload.name,
        node_type=payload.node_type.value,
        description=payload.description,
    )

    db.add(node)
    db.commit()
    db.refresh(node)

    return node


@router.get("", response_model=list[NodeRead])
def list_nodes(db: Session = Depends(get_db)):
    return db.scalars(select(Node).order_by(Node.name)).all()


@router.get("/{node_id}", response_model=NodeRead)
def get_node(node_id: int, db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    return node


@router.put("/{node_id}", response_model=NodeRead)
def update_node(node_id: int, payload: NodeUpdate, db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    if payload.name is not None:
        node.name = payload.name

    if payload.node_type is not None:
        node.node_type = payload.node_type.value

    if payload.description is not None:
        node.description = payload.description

    db.commit()
    db.refresh(node)

    return node


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: int, db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    db.delete(node)
    db.commit()

    return None
