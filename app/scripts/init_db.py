from app.database import clickhouse_client


def create_table():
    clickhouse_client.command("DROP TABLE IF EXISTS documents")
    clickhouse_client.command("""
        CREATE TABLE documents (
            id UUID DEFAULT generateUUIDv4(),
            rubrics Array(String),
            text String,
            created_date DateTime
        )
        ENGINE = MergeTree()
        ORDER BY created_date
    """)

    print("Таблица documents создана")


if __name__ == "__main__":
    create_table()