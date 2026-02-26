import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection
db_connection_str = 'postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide'

def fetch_data():
    try:
        engine = create_engine(db_connection_str)
        
        # Query for non-cancelled trips with hotel data
        # We join sessions with hotels and flights to get pricing info
        query = """
        SELECT 
            s.session_id, 
            s.user_id, 
            s.trip_id, 
            s.session_start, 
            s.cancellation,
            s.hotel_booked, 
            s.flight_booked, 
            s.hotel_discount, 
            s.hotel_discount_amount,
            h.hotel_name, 
            h.nights, 
            h.rooms, 
            h.check_in_time, 
            h.hotel_per_room_usd,
            h.hotel_per_room_usd,
            f.base_fare_usd,
            f.seats,
            f.trip_airline,
            f.return_flight_booked
        FROM sessions s
        LEFT JOIN hotels h ON s.trip_id = h.trip_id
        LEFT JOIN flights f ON s.trip_id = f.trip_id
        WHERE s.cancellation = FALSE 
        AND s.trip_id IS NOT NULL
        LIMIT 50000;
        """
        
        print("Fetching non-cancelled trips (Limited to 50,000 rows for performance)...")
        df = pd.read_sql(query, engine)
        
        # Calculate raw total hotel spend (ignoring discount for a moment, or assuming per_room is base)
        # hotel_spend = nights * rooms * hotel_per_room_usd
        # We will handle this in the analysis, but good to have the raw columns.
        
        os.makedirs('data', exist_ok=True)
        output_path = 'data/non_cancelled_trips.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} rows to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_data()
