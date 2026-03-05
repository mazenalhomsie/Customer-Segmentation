import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_connection_str = os.environ.get('DATABASE_URL')
if db_connection_str and db_connection_str.startswith("postgresql://"):
    db_connection_str = db_connection_str.replace("postgresql://", "postgres://", 1)

def check_counts():
    try:
        conn = psycopg2.connect(db_connection_str)
        cur = conn.cursor()
        
        tables = ['hotels', 'users', 'flights', 'sessions']
        
        print("Table Row Counts:")
        for table in tables:
            cur.execute(f"SELECT count(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"{table}: {count}")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_counts()
