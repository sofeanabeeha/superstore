import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "superstore.csv"

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

def import_csv():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set."
        )

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"superstore.csv was not found at {CSV_PATH}"
        )

    dataframe = pd.read_csv(
        CSV_PATH,
        encoding="latin-1"
    )

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    for column in ["order_date", "ship_date"]:
        if column in dataframe.columns:
            dataframe[column] = pd.to_datetime(
                dataframe[column],
                errors="coerce"
            )

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

    dataframe.to_sql(
        name="superstore_orders",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=500
    )

    with engine.connect() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM superstore_orders")
        ).scalar_one()

    print(
        f"Import completed successfully. "
        f"{row_count} rows were added."
    )


if __name__ == "__main__":
    import_csv()