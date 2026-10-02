import json
from main import app


def generate_openapi():

    openapi_schema = app.openapi()

    with open("docs.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

    print("OpenAPI схема сохранена в docs.json")


if __name__ == "__main__":
    generate_openapi()