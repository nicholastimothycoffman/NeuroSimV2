from pydantic import BaseModel, ConfigDict

from app.relationships.models import RelationshipType


class RelationshipCreate(BaseModel):
    source_node_id: int
    target_node_id: int
    relationship_type: RelationshipType
    description: str | None = None
    weight: float = 1.0
    evidence_level: str | None = None


class RelationshipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_node_id: int
    target_node_id: int
    relationship_type: str
    description: str | None = None
    weight: float
    evidence_level: str | None = None
