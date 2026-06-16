from pydantic import BaseModel, ConfigDict

from app.nodes.models import NodeType


class NodeCreate(BaseModel):
    name: str
    node_type: NodeType
    description: str | None = None


class NodeUpdate(BaseModel):
    name: str | None = None
    node_type: NodeType | None = None
    description: str | None = None


class NodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    node_type: str
    description: str | None = None
