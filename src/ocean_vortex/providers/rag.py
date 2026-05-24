from typing import Any

from pydantic import BaseModel


class Document(BaseModel):
    page_content: str
    metadata: dict[str, Any]

MOCK_S3_BUCKET = [
    Document(
        page_content="Carnival Corporation enforces the 'Less Left Over' food management program. This uses AI-powered predictive systems to manage food production, prioritizing waste reduction. When recommending food, advise guests about our sustainable dining options.",
        metadata={"source": "s3://carnival-policies/environmental/less_left_over.md", "topic": "Food & Beverage"}
    ),
    Document(
        page_content="Maritime Safety Guidelines (OHSAS 18001:2007): All shore excursions involving water activities (like snorkeling or scuba diving) must be paired with an automated digital safety briefing delivered via the OceanMedallion ecosystem. Guests with high blood pressure or heart conditions should be advised against high-intensity water activities.",
        metadata={"source": "s3://carnival-policies/safety/excursions_water.md", "topic": "Safety"}
    ),
    Document(
        page_content="White Star Service Standard: When interacting with VIP guests (e.g., Ruby or Diamond Medallion Status), responses should be highly refined, charismatic, and prioritize anticipatory service.",
        metadata={"source": "s3://carnival-policies/service/white_star.md", "topic": "Service Standards"}
    )
]

class CortexRAGPipeline:
    """
    Mock RAG Pipeline to simulate Snowflake Cortex AI vector search.
    In a real implementation, this would connect to Snowflake ML/Vector capabilities 
    or AWS SageMaker endpoints to fetch embeddings and run cosine similarity.
    """
    def __init__(self) -> None:
        # We would normally initialize ChromaDB or Snowflake connection here.
        self.documents = MOCK_S3_BUCKET

    def retrieve_context(self, query: str, top_k: int = 2) -> list[Document]:
        """
        Simulate semantic search. 
        For this mock, we use a simple keyword matching heuristic, but it represents
        a vector similarity search that would happen in Cortex AI.
        """
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            score = 0
            # Simple keyword overlap simulation
            if "food" in query_lower or "eat" in query_lower or "drink" in query_lower:
                if doc.metadata["topic"] == "Food & Beverage":
                    score += 2
            if "snorkeling" in query_lower or "water" in query_lower or "excursion" in query_lower:
                if doc.metadata["topic"] == "Safety":
                    score += 2
            if "vip" in query_lower or "service" in query_lower:
                if doc.metadata["topic"] == "Service Standards":
                    score += 2
            
            scored_docs.append((score, doc))
        
        # Sort by score descending and return top_k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]

# Singleton instance
rag_pipeline = CortexRAGPipeline()
