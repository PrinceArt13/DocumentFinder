from fastapi import APIRouter, Query
from typing import List
from app.models.document import Document
from app.services.search_service import search_documents

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.get(
    "/search",
    response_model=List[Document],
    summary="Поиск документов",
    description="Поиск документов по тексту. Возвращает документы, упорядоченные по дате создания."
)
async def search(
        query: str = Query(..., description="Текстовый запрос для поиска")
):
    documents = await search_documents(query)
    return documents