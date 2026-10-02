# Document Search API

Поисковик по текстам документов с использованием ElasticSearch.

## Описание

Сервис принимает текстовый запрос, ищет по тексту документа в Elasticsearch и возвращает документы, упорядоченные по дате создания. 
Также поддерживает удаление документов из БД и индекса.

## Стек технологий

- **Python 3.10+**
- **FastAPI** — веб-фреймворк
- **ClickHouse** — основная БД для хранения документов
- **Elasticsearch** — поисковый индекс
- **Docker & Docker Compose** — контейнеризация БД и Elasticsearch
- **Pydantic** — валидация данных
- **pandas** — импорт CSV данных


## Требования

- Python 3.10+
- Docker и Docker Compose
- Git (опционально)

## Установка и запуск

### 1. Клонировать репозиторий и перейти в директорию

```bash
cd DocumentFinder
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения
Создайте файл `.env` в корне проекта и заполните его, исходя из .env.example

### 4. Запустить ClickHouse и Elasticsearch через Docker

```bash
docker-compose up -d
```

### 5. Запуск скриптов

```bash
# Создание таблицы в БД
python app/scripts/init_db.py
# Импорт CSV
python app/scripts/import_csv.py
# Индексация документов в Elasticsearch
python app/scripts/index_documents.py
# Генерация OPENAPI
python app/scripts/generate_openapi.py
```

### 6. Запустить FastAPI приложение

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Поиск документов

**GET** `/documents/search?query={text}`

Поиск документов по тексту.

**Пример запроса:**

```bash
curl "http://127.0.0.1:8000/documents/search?query=привет"
```

**Пример ответа:**

```json
[
  {
    "rubrics": [
      "VK-1603736028819866",
      "VK-88098320357",
      "VK-13827004574"
    ],
    "text": "всем привет кто-то переделывал старый спринтер 1996 года  на 906й ? двери салон и буду хочу оставить . приколхозить только морду.  жду ответа",
    "created_date": "2019-12-27T15:06:19",
    "id": "42105b22-7f2e-453e-8eb6-b57266425d76"
  }
]
```

### Удаление документа

**DELETE** `/documents/{document_id}`

Удаляет документ по UUID.

**Пример запроса:**

```bash
curl -X DELETE "http://127.0.0.1:8000/documents/3e7632bd-630d-44fd-a7f2-b8da5e5da786"
```

**Пример ответа:**

```json
{
  "success": true,
  "message": "Документ 3e7632bd-630d-44fd-a7f2-b8da5e5da786 успешно удалён"
}
```

## Тесты
```bash
pytest -v -s
```

## Интерактивная документация

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Остановка сервисов

```bash
# Остановить контейнеры
docker-compose down

# Остановить и удалить volumes (полная очистка)
docker-compose down -v
```