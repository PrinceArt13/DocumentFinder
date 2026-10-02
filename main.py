from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.elasticsearch import es_client
from app.routers import search, delete


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await es_client.close()


app = FastAPI(
    title="Document Search API",
    description="Поисковик по текстам документов",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(search.router)
app.include_router(delete.router)


@app.get("/", tags=["root"])
def root():
    return {"message": "app is running"}
