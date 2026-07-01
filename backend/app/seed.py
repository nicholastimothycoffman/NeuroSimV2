from app.core.database import SessionLocal
from app.nodes.models import Node
from app.relationships.models import Relationship


def seed_database():
    db = SessionLocal()

    try:
        existing_nodes = db.query(Node).count()
        if existing_nodes > 0:
            print("Database already contains data. Seed skipped.")
            return

        nodes = [
            Node(name="Stress", node_type="cognitive_state", description="A state of psychological or physiological strain."),
            Node(name="Working Memory", node_type="cognitive_function", description="Temporary holding and manipulation of information."),
            Node(name="Attention", node_type="cognitive_function", description="Selective focus on relevant information."),
            Node(name="Flow", node_type="cognitive_state", description="Highly focused and absorbed performance state."),
            Node(name="Sleep", node_type="factor", description="Restorative biological process supporting cognition."),
            Node(name="Creativity", node_type="outcome", description="Generation of novel and useful ideas."),
            Node(name="Motivation", node_type="factor", description="Drive toward action or goal pursuit."),
            Node(name="Anxiety", node_type="cognitive_state", description="State of apprehension or worry."),
            Node(name="Cognitive Load", node_type="factor", description="Mental effort imposed by a task."),
            Node(name="Context Window", node_type="ai_analogue", description="Amount of information an AI model can attend to at once."),
        ]

        db.add_all(nodes)
        db.commit()

        node_map = {node.name: node for node in db.query(Node).all()}

        relationships = [
            Relationship(
                source_node_id=node_map["Stress"].id,
                target_node_id=node_map["Working Memory"].id,
                relationship_type="impairs",
                weight=0.8,
                evidence_level="moderate",
            ),
            Relationship(
                source_node_id=node_map["Stress"].id,
                target_node_id=node_map["Attention"].id,
                relationship_type="reduces",
                weight=0.7,
                evidence_level="moderate",
            ),
            Relationship(
                source_node_id=node_map["Sleep"].id,
                target_node_id=node_map["Attention"].id,
                relationship_type="supports",
                weight=0.8,
                evidence_level="strong",
            ),
            Relationship(
                source_node_id=node_map["Sleep"].id,
                target_node_id=node_map["Working Memory"].id,
                relationship_type="improves",
                weight=0.75,
                evidence_level="strong",
            ),
            Relationship(
                source_node_id=node_map["Flow"].id,
                target_node_id=node_map["Creativity"].id,
                relationship_type="enhances",
                weight=0.7,
                evidence_level="moderate",
            ),
            Relationship(
                source_node_id=node_map["Working Memory"].id,
                target_node_id=node_map["Context Window"].id,
                relationship_type="analogous_to",
                weight=0.6,
                evidence_level="conceptual",
            ),
            Relationship(
                source_node_id=node_map["Motivation"].id,
                target_node_id=node_map["Flow"].id,
                relationship_type="promotes",
                weight=0.65,
                evidence_level="moderate",
            ),
            Relationship(
                source_node_id=node_map["Anxiety"].id,
                target_node_id=node_map["Stress"].id,
                relationship_type="increases",
                weight=0.75,
                evidence_level="moderate",
            ),
        ]

        db.add_all(relationships)
        db.commit()

        print("Seed data inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
