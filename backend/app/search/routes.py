from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.nodes.models import Node
from app.nodes.schemas import NodeRead

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/nodes", response_model=list[NodeRead])
def search_nodes(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    pattern = f"%{q}%"

    return db.scalars(
        select(Node)
        .where(
            or_(
                Node.name.ilike(pattern),
                Node.description.ilike(pattern),
                Node.node_type.ilike(pattern),
            )
        )
        .order_by(Node.name)
    ).all()
