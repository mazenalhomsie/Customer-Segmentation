import pandas as pd
import pytest
import os

# Data paths
TRIPS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'not_canceled_trips.csv')
SESSIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'session_base.csv')

@pytest.fixture
def trips_data():
    if not os.path.exists(TRIPS_PATH):
        pytest.skip(f"Data file {TRIPS_PATH} not found. Run preprocessing first.")
    return pd.read_csv(TRIPS_PATH)

@pytest.fixture
def sessions_data():
    if not os.path.exists(SESSIONS_PATH):
        pytest.skip(f"Data file {SESSIONS_PATH} not found. Run preprocessing first.")
    return pd.read_csv(SESSIONS_PATH)


def test_no_swapped_dates_in_trips(trips_data):
    """Prüft, ob alle check_out_time chronologisch nach check_in_time liegen."""
    if 'check_in_time' in trips_data.columns and 'check_out_time' in trips_data.columns:
        trips_data['check_in_time'] = pd.to_datetime(trips_data['check_in_time'])
        trips_data['check_out_time'] = pd.to_datetime(trips_data['check_out_time'])
        
        # Datensätze mit gültigen Hotel-Daten (wo Check-In / Check-Out existieren)
        valid_hotels = trips_data.dropna(subset=['check_in_time', 'check_out_time'])
        
        errors = valid_hotels[valid_hotels['check_out_time'] < valid_hotels['check_in_time']]
        assert len(errors) == 0, f"Gefunden: {len(errors)} Einträge mit vertauschten Check-In/Out Zeiten!"

def test_no_zero_nights_for_booked_hotels(trips_data):
    """Prüft, ob bei allen Hotelbuchungen (hotel_booked=True) mindestens 1 Nacht verbracht wurde."""
    if 'hotel_booked' in trips_data.columns and 'nights' in trips_data.columns:
        zero_nights = trips_data[(trips_data['hotel_booked'] == True) & (trips_data['nights'] == 0)]
        assert len(zero_nights) == 0, f"Gefunden: {len(zero_nights)} Hotelbuchungen mit 0 Nächten!"

def test_negative_nights_fixed(trips_data):
    """Prüft, ob keine negativen Nächte existieren."""
    if 'nights' in trips_data.columns:
        negative_nights = trips_data[trips_data['nights'] < 0]
        assert len(negative_nights) == 0, f"Gefunden: {len(negative_nights)} Einträge mit negativen Nächten!"

def test_no_zero_seats_for_booked_flights(trips_data):
    """Prüft, ob bei allen Flugbuchungen (flight_booked=True) mindestens 1 Sitzplatz gebucht ist."""
    if 'flight_booked' in trips_data.columns and 'seats' in trips_data.columns:
        zero_seats = trips_data[(trips_data['flight_booked'] == True) & (trips_data['seats'] == 0)]
        assert len(zero_seats) == 0, f"Gefunden: {len(zero_seats)} Flugbuchungen mit 0 Sitzplätzen!"

def test_page_clicks_not_negative(sessions_data):
    """Prüft, ob die Anzahl der Klicks niemals negativ ist."""
    if 'page_clicks' in sessions_data.columns:
        negative_clicks = sessions_data[sessions_data['page_clicks'] < 0]
        assert len(negative_clicks) == 0, f"Gefunden: {len(negative_clicks)} Sessions mit negativen Klicks!"

def test_no_canceled_trips_in_target(trips_data):
    """Prüft, ob im Datensatz für angetretene Reisen keine stornierten Buchungen existieren."""
    if 'cancellation' in trips_data.columns:
        canceled = trips_data[trips_data['cancellation'] == True]
        assert len(canceled) == 0, f"Echter Fehler: {len(canceled)} stornierte Reisen im not_canceled_trips-Datensatz!"
