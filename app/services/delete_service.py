import uuid
from app.elasticsearch import es_client
from app.database import clickhouse_client
from app.config import settings


async def delete_document(document_id: uuid.UUID) -> bool:
    clickhouse_client.command(f"""
        ALTER TABLE documents DELETE WHERE id = '{document_id}'
    """)

    try:
        await es_client.delete(
            index=settings.elasticsearch_index,
            id=str(document_id)
        )
        return True
    except Exception as e:
        print(f"Предупреждение при удалении из Elasticsearch: {e}")
        return True
