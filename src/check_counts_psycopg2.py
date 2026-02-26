import psycopg2

db_connection_str = 'postgres://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'

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
