from elasticsearch import AsyncElasticsearch

from app.config import settings


def get_elasticsearch_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(
        hosts=[
            {
                "host": settings.elasticsearch_host,
                "port": settings.elasticsearch_port,
                "scheme": "http",
            }
        ],
        basic_auth=(settings.elasticsearch_user, settings.elasticsearch_password),
    )


es_client = get_elasticsearch_client()