import uuid
from fastapi import APIRouter, HTTPException
from app.models.document import DocumentDeleteResponse
from app.services.delete_service import delete_document

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.delete(
    "/{document_id}",
    response_model=DocumentDeleteResponse,
    summary="Удалить документ",
    description="Удалить документ из БД и поискового индекса по ID"
)
async def delete(document_id: uuid.UUID):
    success = await delete_document(document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Документ не найден")

    return DocumentDeleteResponse(
        success=True,
        message=f"Документ {document_id} успешно удалён"
    )