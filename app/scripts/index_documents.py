import asyncio

from elasticsearch.helpers import async_bulk
from app.database import clickhouse_client
from app.elasticsearch import es_client
from app.config import settings


async def create_index():
    index_name = settings.elasticsearch_index
    if await es_client.indices.exists(index=index_name):
        await es_client.indices.delete(index=index_name)
        print(f"Индекс {index_name} удалён")

    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "text": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                }
            }
        }
    }

    await es_client.indices.create(index=index_name, body=mapping)
    print(f"Индекс {index_name} создан")


async def index_documents():
    result = clickhouse_client.query("""
        SELECT id, text
        FROM documents
    """)

    documents = []
    for row in result.result_rows:
        documents.append({
            "_index": settings.elasticsearch_index,
            "_id": str(row[0]),
            "_source": {
                "id": str(row[0]),
                "text": row[1]
            }
        })

    print(f"Найдено {len(documents)} документов")
    success, failed = await async_bulk(
        es_client.options(request_timeout=60),
        documents,
        chunk_size=500,
    )

    print(f"Успешно проиндексировано: {success}")
    if failed:
        print(f"Ошибок: {len(failed)}")
        for error in failed:
            print(f"  {error}")


async def main():
    try:
        await create_index()
        await index_documents()
    finally:
        await es_client.close()


if __name__ == "__main__":
    asyncio.run(main())