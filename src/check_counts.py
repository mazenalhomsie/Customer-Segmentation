import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()
db_connection_str = os.environ.get('DATABASE_URL')

def get_row_counts():
    try:
        engine = create_engine(db_connection_str)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("Table Row Counts:")
        for table in tables:
            query = f"SELECT count(*) FROM {table}"
            count = pd.read_sql(query, engine).iloc[0, 0]
            print(f"{table}: {count}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_row_counts()
