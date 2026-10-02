from typing import List
from app.elasticsearch import es_client
from app.database import clickhouse_client
from app.config import settings
from app.models.document import Document


async def search_documents(query: str) -> List[Document]:
    search_result = await es_client.search(
        index=settings.elasticsearch_index,
        body={
            "query": {
                "match": {
                    "text": query
                }
            }
        }
    )

    doc_ids = [hit["_id"] for hit in search_result["hits"]["hits"]]

    if not doc_ids:
        return []

    ids_str = ", ".join([f"'{id}'" for id in doc_ids])

    result = clickhouse_client.query(f"""
        SELECT id, rubrics, text, created_date
        FROM documents
        WHERE id IN ({ids_str})
        ORDER BY created_date DESC
    """)

    documents = []
    for row in result.result_rows:
        documents.append(Document(
            id=row[0],
            rubrics=row[1],
            text=row[2],
            created_date=row[3]
        ))

    return documents
