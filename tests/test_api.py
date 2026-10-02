import pytest

@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "app is running"}


@pytest.mark.asyncio
async def test_search_documents(async_client):
    response = await async_client.get("/documents/search?query=привет")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first_doc = data[0]
    assert "id" in first_doc
    assert "rubrics" in first_doc
    assert "text" in first_doc
    assert "created_date" in first_doc
    assert isinstance(first_doc["rubrics"], list)


@pytest.mark.asyncio
async def test_search_and_delete_document(async_client):
    search_response = await async_client.get("/documents/search?query=привет")
    docs = search_response.json()

    assert len(docs) > 0, "Не найдено документов для удаления"
    doc_id = docs[0]["id"]

    delete_response = await async_client.delete(f"/documents/{doc_id}")

    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["success"] is True
    assert "успешно удалён" in delete_data["message"]


@pytest.mark.asyncio
async def test_delete_non_existent_document(async_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.delete(f"/documents/{fake_id}")
    assert response.status_code in [200, 404]