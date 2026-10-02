import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class DocumentBase(BaseModel):
    rubrics: List[str] = Field(..., description="Массив рубрик")
    text: str = Field(..., description="Текст документа")
    created_date: datetime = Field(..., description="Дата создания документа")


class Document(DocumentBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID = Field(..., description="ID документа")


class DocumentSearchResponse(BaseModel):
    documents: List[Document] = Field(..., description="Список найденных документов")
    total: int = Field(..., description="Общее количество найденных документов")


class DocumentDeleteResponse(BaseModel):
    success: bool = Field(..., description="Успешность операции")
    message: str = Field(..., description="Сообщение о результате")