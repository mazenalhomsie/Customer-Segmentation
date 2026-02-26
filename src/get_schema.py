import psycopg2

db_connection_str = 'postgres://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'

def get_schema():
    try:
        conn = psycopg2.connect(db_connection_str)
        cur = conn.cursor()
        
        tables = ['hotels', 'users', 'flights', 'sessions']
        
        print("Schema Information:")
        for table in tables:
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'")
            columns = cur.fetchall()
            print(f"\nTable: {table}")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_schema()
