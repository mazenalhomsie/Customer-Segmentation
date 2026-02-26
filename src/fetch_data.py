import os
from sqlalchemy import create_engine, inspect
import pandas as pd

# Database connection string
db_connection_str = 'postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'
db_connection_str = db_connection_str.replace("postgres://", "postgresql://")

def fetch_data():
    try:
        # Create database engine
        engine = create_engine(db_connection_str)
        inspector = inspect(engine)
        
        # Get list of tables
        table_names = inspector.get_table_names()
        print(f"Found tables: {table_names}")
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        for table in table_names:
            print(f"Fetching table: {table}...")
            df = pd.read_sql_table(table, engine)
            output_file = f'data/{table}.csv'
            df.to_csv(output_file, index=False)
            print(f"Saved {table} to {output_file} ({len(df)} rows)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_data()
