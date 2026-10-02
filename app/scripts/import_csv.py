import ast
import pandas as pd
from app.database import clickhouse_client
from app.config import settings


def parse_rubrics(rubrics_str):
    if pd.isna(rubrics_str) or not rubrics_str:
        return []

    rubrics_str = str(rubrics_str).strip()
    if rubrics_str.startswith('[') and rubrics_str.endswith(']'):
        try:
            result = ast.literal_eval(rubrics_str)
            if isinstance(result, list):
                return [str(r) for r in result]
        except (ValueError, SyntaxError):
            pass

        inner = rubrics_str[1:-1]
        return [r.strip().strip("'\"") for r in inner.split(',') if r.strip()]

    return [rubrics_str]


def import_csv():
    file_path = settings.csv_file_path
    df = pd.read_csv(file_path)
    df['rubrics'] = df['rubrics'].apply(parse_rubrics)

    df['created_date'] = pd.to_datetime(df['created_date'])

    data = [
        (
            row['rubrics'],
            row['text'],
            row['created_date']
        )
        for _, row in df.iterrows()
    ]
    clickhouse_client.command("TRUNCATE TABLE documents")
    print("Таблица очищена")

    clickhouse_client.insert(
        'documents',
        data,
        column_names=['rubrics', 'text', 'created_date']
    )

    print(f"Успешно импортировано {len(df)} документов")


if __name__ == "__main__":
    import_csv()
