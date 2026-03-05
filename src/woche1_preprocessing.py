import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen (z.B. DATABASE_URL)
load_dotenv()
db_connection_str = os.getenv('DATABASE_URL')
# Korrigiere postgres:// zu postgresql:// für SQLAlchemy
if db_connection_str and db_connection_str.startswith("postgres://"):
    db_connection_str = db_connection_str.replace("postgres://", "postgresql://", 1)

def run_preprocessing(sample_size=150000):
    try:
        engine = create_engine(db_connection_str)
        os.makedirs('data', exist_ok=True)
        
        print(f"Starte Data Preprocessing (Woche 1) mit {sample_size} Datensätzen...")
        
        # 1. Cohort Filtering & Data Processing in SQL
        # Wir laden Nutzer-Sessions ab '2023-01-04'
        
        # Negative Nächte (nights) beheben wir via ABS(h.nights)
        query = f"""
        WITH CohortUsers AS (
            SELECT user_id 
            FROM sessions 
            WHERE session_start >= '2023-01-04'
            GROUP BY user_id
            HAVING COUNT(session_id) > 7
        )
        SELECT 
            s.session_id,
            s.user_id,
            s.trip_id,
            s.session_start,
            s.session_end,
            s.flight_discount,
            s.hotel_discount,
            s.flight_discount_amount,
            s.hotel_discount_amount,
            s.flight_booked,
            s.hotel_booked,
            s.page_clicks,
            s.cancellation,
            f.origin_airport,
            f.destination,
            f.destination_airport,
            f.seats,
            f.return_flight_booked,
            f.departure_time,
            f.return_time,
            f.checked_bags,
            f.trip_airline,
            f.destination_airport_lat,
            f.destination_airport_lon,
            f.base_fare_usd,
            h.hotel_name,
            -- Negative Nächte behandeln (aus z.B. -2 wird 2)
            ABS(h.nights) AS nights,
            h.rooms,
            h.check_in_time,
            h.check_out_time,
            h.hotel_per_room_usd
        FROM sessions s
        JOIN CohortUsers cu ON s.user_id = cu.user_id
        LEFT JOIN flights f ON s.trip_id = f.trip_id
        LEFT JOIN hotels h ON s.trip_id = h.trip_id
        LIMIT {sample_size};
        """
        
        print("Lade Daten aus DB (dauert evt. ein paar Sekunden)...")
        df = pd.read_sql(query, engine)
        
        # 2. Ausreißer erkennen & behandeln
        print("Erkenne und behandle Ausreißer in 'base_fare_usd' & 'page_clicks'...")
        # Negative Base Fares auf 0 beschränken (falls fehlerhaft)
        df['base_fare_usd'] = df['base_fare_usd'].apply(lambda x: max(0, x) if pd.notnull(x) else x)
        
        # Extreme "page_clicks"-Werte mit der IQR-Methode (Interquartile Range) abfangen und "cappen"
        Q1 = df['page_clicks'].quantile(0.25)
        Q3 = df['page_clicks'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        df['page_clicks'] = df['page_clicks'].clip(upper=upper_bound)
        
        # Die Interaktionen zwischen Buchung und Stornierung kann man hier ableiten: 
        # Falls canceled == True, hat der User zwar interagiert, aber am Ende storniert.
        
        # 3. session_base.csv exportieren
        session_base_cols = [
            'session_id', 'user_id', 'trip_id', 'session_start', 'session_end',
            'flight_discount', 'hotel_discount', 'flight_discount_amount', 
            'hotel_discount_amount', 'flight_booked', 'hotel_booked', 
            'page_clicks', 'cancellation'
        ]
        session_base = df[session_base_cols].copy()
        session_path = 'data/session_base.csv'
        session_base.to_csv(session_path, index=False)
        print(f"Gespeichert: {session_path} (Sessions/Iteraktionen, {len(session_base)} Zeilen)")
        
        # 4. not_canceled_trips.csv exportieren
        # Trips beibehalten, insofern sie nicht storniert wurden UND Hotel/Flug gebucht wurde!
        not_canceled = df[
            (df['cancellation'] == False) & 
            (df['flight_booked'] | df['hotel_booked']) &
            (df['trip_id'].notnull())
        ].copy()
        
        # --- Zusätzliche Fehlerbehandlung für angetretene Reisen ---
        print("Vor Fehlerbehebung in Reisendaten...")
        
        # A. Vertauschte Check-in / Check-out Zeiten tauschen (Hotel)
        # Wir müssen sicherstellen, dass wir datetime-Objekte haben
        not_canceled['check_in_time'] = pd.to_datetime(not_canceled['check_in_time'])
        not_canceled['check_out_time'] = pd.to_datetime(not_canceled['check_out_time'])
        
        mask_swapped = not_canceled['check_out_time'] < not_canceled['check_in_time']
        if mask_swapped.sum() > 0:
            print(f"- Korrigiere {mask_swapped.sum()} vertauschte Check-In/Check-Out Daten.")
            temp_checkin = not_canceled.loc[mask_swapped, 'check_in_time'].copy()
            not_canceled.loc[mask_swapped, 'check_in_time'] = not_canceled.loc[mask_swapped, 'check_out_time']
            not_canceled.loc[mask_swapped, 'check_out_time'] = temp_checkin
            
        # B. 0 Nächte trotz Hotelbuchung auf mindestens 1 setzen
        mask_0_nights = (not_canceled['hotel_booked'] == True) & (not_canceled['nights'] == 0)
        if mask_0_nights.sum() > 0:
            print(f"- Korrigiere {mask_0_nights.sum()} Hotelbuchungen mit 0 Nächten zu 1.")
            not_canceled.loc[mask_0_nights, 'nights'] = 1
            
        # C. 0 Sitze trotz Flugbuchung auf mindestens 1 setzen
        mask_0_seats = (not_canceled['flight_booked'] == True) & (not_canceled['seats'] == 0)
        if mask_0_seats.sum() > 0:
            print(f"- Korrigiere {mask_0_seats.sum()} Flugbuchungen mit 0 Sitzen zu 1.")
            not_canceled.loc[mask_0_seats, 'seats'] = 1

        
        not_canceled_path = 'data/not_canceled_trips.csv'
        not_canceled.to_csv(not_canceled_path, index=False)
        print(f"Gespeichert: {not_canceled_path} (Nur angetretene Reisen, {len(not_canceled)} Zeilen)")
        
        print("\n✅ Woche 1: Preprocessing & Cohort Filtering fertig!")
        
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    run_preprocessing(150000)
