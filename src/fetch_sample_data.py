import os
from sqlalchemy import create_engine, inspect
import pandas as pd

# Database connection string
db_connection_str = 'postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'

def fetch_sample_data(sample_size=10000):
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
            print(f"Fetching sample from table: {table}...")
            # UseLIMIT to fetch sample
            query = f"SELECT * FROM {table} LIMIT {sample_size}"
            df = pd.read_sql(query, engine)
            
            output_file = f'data/{table}_sample.csv'
            df.to_csv(output_file, index=False)
            print(f"Saved {table} sample to {output_file} ({len(df)} rows)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_sample_data()
