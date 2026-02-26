from sqlalchemy import create_engine, text
import pandas as pd

def get_engine(db_url: str):
    return create_engine(db_url)

def run_query(engine, sql: str) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)
