import pandas as pd
import numpy as np
import os

def run_feature_engineering():
    print("Starte Woche 2: Feature Engineering auf User-Level...")
    
    # Pfade
    sessions_path = 'data/session_base.csv'
    trips_path = 'data/not_canceled_trips.csv'
    
    if not os.path.exists(sessions_path) or not os.path.exists(trips_path):
        print("Fehler: CSV Dateien aus Woche 1 fehlen in 'data/'. Bitte zuerst woche1_preprocessing.py ausführen.")
        return
        
    print("Lade Datensätze...")
    sessions = pd.read_csv(sessions_path)
    trips = pd.read_csv(trips_path)
    
    print(f"Sessions: {len(sessions)}, Trips: {len(trips)}")
    
    # ---------------------------------------------------------------------
    # 1. FEATURES AUS SESSIONS ERSTELLEN (Für alle User)
    # ---------------------------------------------------------------------
    print("Erstelle Features aus Sessions...")
    
    # Boolean Spalten sicher als Bool/Int verarbeiten
    sessions['cancellation'] = sessions['cancellation'].astype(int)
    sessions['is_window_shopping'] = ((sessions['flight_booked'] == False) & (sessions['hotel_booked'] == False)).astype(int)
    
    sessions['has_discount'] = (sessions['flight_discount'] | sessions['hotel_discount']).astype(int)
    
    user_sessions = sessions.groupby('user_id').agg(
        total_sessions=('session_id', 'count'),
        total_cancellations=('cancellation', 'sum'),
        window_shopping_sessions=('is_window_shopping', 'sum'),
        total_discount_sessions=('has_discount', 'sum'),
        total_page_clicks=('page_clicks', 'sum'),
        avg_page_clicks=('page_clicks', 'mean'),
        birthdate=('birthdate', 'first'),
        gender=('gender', 'first'),
        married=('married', 'first'),
        has_children=('has_children', 'first')
    ).reset_index()
    
    # Ratios berechnen
    user_sessions['cancellation_rate'] = user_sessions['total_cancellations'] / user_sessions['total_sessions']
    user_sessions['window_shopping_rate'] = user_sessions['window_shopping_sessions'] / user_sessions['total_sessions']
    user_sessions['discount_affinity'] = user_sessions['total_discount_sessions'] / user_sessions['total_sessions']
    
    # Demografische Features konvertieren
    reference_date = pd.to_datetime('2026-01-01') # Statisches Datum für das Projekt Alter
    user_sessions['age'] = (reference_date - pd.to_datetime(user_sessions['birthdate'], errors='coerce')).dt.days // 365
    user_sessions['is_married'] = user_sessions['married'].fillna(False).astype(int)
    user_sessions['has_kids'] = user_sessions['has_children'].fillna(False).astype(int)
    
    # Füllen von NaN bei age mit dem Median
    user_sessions['age'] = user_sessions['age'].fillna(user_sessions['age'].median())
    
    # Drop original demografische text Spalten
    user_sessions.drop(columns=['birthdate', 'gender', 'married', 'has_children'], inplace=True)
    
    # ---------------------------------------------------------------------
    # 2. FEATURES AUS TRIPS ERSTELLEN (Nur für User mit angetretenen Reisen)
    # ---------------------------------------------------------------------
    print("Erstelle Features aus durchgeführten Trips...")
    
    # Kosten berechnen 
    # Flugkosten (base_fare_usd nehmen wir als Gesamtkosten des Flugs an)
    trips['flight_cost'] = trips['base_fare_usd'].fillna(0)
    
    # Hotelkosten: Preis pro Zimmer * Zimmeranzahl * Nächte
    trips['hotel_cost'] = (trips['hotel_per_room_usd'] * trips['rooms'] * trips['nights']).fillna(0)
    
    # Gesamtkosten der Reise
    trips['trip_total_cost'] = trips['flight_cost'] + trips['hotel_cost']
    
    # Annahmen über Kunden treffen (z.B. Business Trip)
    # Business-Trip Annahme: Fliegt alleine (1 Seat) UND wenig/kein Aufgabegepäck (<=1) UND eher kurz (Nights <= 3)
    trips['is_business_trip'] = (
        (trips['flight_booked'] == True) & 
        (trips['seats'] == 1) & 
        (trips['checked_bags'].fillna(0) <= 1) &
        (trips['nights'].fillna(0) <= 3)
    ).astype(int)
    
    # Family-Trip Annahme: Mehr als 2 Sitze oder mehr als 1 Zimmer
    trips['is_family_trip'] = (
        (trips['seats'] > 2) | 
        (trips['rooms'] > 1)
    ).astype(int)
    
    # Vorlaufzeit der Buchung berechnen (Booking Lead Time)
    trips['session_start'] = pd.to_datetime(trips['session_start'])
    trips['flight_start'] = pd.to_datetime(trips['departure_time'])
    trips['hotel_start'] = pd.to_datetime(trips['check_in_time'])
    
    # Frühester Reisebeginn (entweder Flug oder Hotel)
    trips['travel_start'] = trips[['flight_start', 'hotel_start']].min(axis=1)
    
    # Differenz in Tagen (Lead Time)
    trips['booking_lead_time'] = (trips['travel_start'] - trips['session_start']).dt.days
    trips['booking_lead_time'] = trips['booking_lead_time'].fillna(0) # Fallback
    
    # Trip-Daten aggregieren
    user_trips = trips.groupby('user_id').agg(
        total_trips=('trip_id', 'count'),
        total_spent=('trip_total_cost', 'sum'),
        avg_spent_per_trip=('trip_total_cost', 'mean'),
        avg_nights_hotel=('nights', 'mean'),
        avg_booking_lead_time=('booking_lead_time', 'mean'),
        total_business_trips=('is_business_trip', 'sum'),
        total_family_trips=('is_family_trip', 'sum')
    ).reset_index()
    
    # ---------------------------------------------------------------------
    # 3. ZUSAMMENFÜHREN (MERGE)
    # ---------------------------------------------------------------------
    print("Führe Session- und Trip-Features zusammen (User-Level)...")
    
    # Left Join: Wir behalten alle Nutzer (auch die, die nur Window-Shopping gemacht haben)
    user_base = pd.merge(user_sessions, user_trips, on='user_id', how='left')
    
    # Fehlende Werte (NaN) bei den Trips für Nutzer auffüllen, die keine Reise gemacht haben
    fill_cols = ['total_trips', 'total_spent', 'avg_spent_per_trip', 'avg_nights_hotel', 'avg_booking_lead_time', 'total_business_trips', 'total_family_trips']
    user_base[fill_cols] = user_base[fill_cols].fillna(0)
    
    # Ratios auf Trip-Level berechnen (vermeide Division durch 0)
    user_base['business_trip_ratio'] = np.where(user_base['total_trips'] > 0, user_base['total_business_trips'] / user_base['total_trips'], 0)
    user_base['family_trip_ratio'] = np.where(user_base['total_trips'] > 0, user_base['total_family_trips'] / user_base['total_trips'], 0)
    
    # ---------------------------------------------------------------------
    # 4. Qualitätskontrolle (Quality Control / QC)
    # ---------------------------------------------------------------------
    print("\n--- Führe Qualitätskontrolle (Missing Values) durch ---")
    missing_final = user_base.isna().sum().sort_values(ascending=False).head(10)
    print("Top-10 Missing-Spalten nach finaler Imputation:")
    print(missing_final.to_string())
    
    if missing_final.sum() == 0:
        print("✅ QC Bestanden: Datensatz ist 100% lückenlos! (Ideal für K-Means)")
    else:
        print("⚠️ QC Warnung: Es gibt noch fehlende Werte im Datensatz!")
    print("-------------------------------------------------------")

    # Export
    output_path = 'data/user_base.csv'
    user_base.to_csv(output_path, index=False)
    
    print(f"\n✅ Woche 2: Feature Engineering fertig! {len(user_base)} Unique Users aggregiert.")
    print(f"Daten gespeichert unter: {output_path}")

if __name__ == "__main__":
    run_feature_engineering()
