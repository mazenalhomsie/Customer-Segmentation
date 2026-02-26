import pandas as pd
from sqlalchemy import create_engine, inspect

db_connection_str = 'postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'

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
