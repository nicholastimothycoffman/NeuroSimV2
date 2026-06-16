from enum import Enum

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class NodeType(str, Enum):
    cognitive_state = "cognitive_state"
    cognitive_function = "cognitive_function"
    factor = "factor"
    outcome = "outcome"
    ai_analogue = "ai_analogue"


class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    node_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    outgoing_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.source_node_id",
        back_populates="source_node",
        cascade="all, delete-orphan",
    )

    incoming_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.target_node_id",
        back_populates="target_node",
        cascade="all, delete-orphan",
    )
