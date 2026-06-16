from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RelationshipType(str, Enum):
    increases = "increases"
    decreases = "decreases"
    requires = "requires"
    impairs = "impairs"
    supports = "supports"
    correlates_with = "correlates_with"
    contributes_to = "contributes_to"
    analogous_to = "analogous_to"
    precedes = "precedes"


class Relationship(Base):
    __tablename__ = "relationships"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    source_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), nullable=False, index=True)
    target_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), nullable=False, index=True)

    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    evidence_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    source_node = relationship(
        "Node",
        foreign_keys=[source_node_id],
        back_populates="outgoing_relationships",
    )

    target_node = relationship(
        "Node",
        foreign_keys=[target_node_id],
        back_populates="incoming_relationships",
    )
