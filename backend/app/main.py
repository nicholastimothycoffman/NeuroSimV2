from fastapi import FastAPI

from app.core.database import Base, engine
from app.graph.routes import router as graph_router
from app.nodes.routes import router as nodes_router
from app.relationships.routes import router as relationships_router
from app.search.routes import router as search_router

# Temporary for early MVP.
# Replace with Alembic migrations soon.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuroSimV2 API",
    description="Cognitive Knowledge Graph Platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(nodes_router)
app.include_router(relationships_router)
app.include_router(graph_router)
app.include_router(search_router)
