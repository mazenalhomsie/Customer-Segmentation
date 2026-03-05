import matplotlib
matplotlib.use('Agg')
print('Backend set to Agg, plots will not block execution.')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Einstellungen für Plots
sns.set_theme(style="whitegrid")
pd.set_option('display.max_columns', None)


# Lade Umgebungsvariablen (z.B. DATABASE_URL)
load_dotenv()
db_connection_str = os.getenv('DATABASE_URL')

# Korrigiere postgres:// zu postgresql:// für SQLAlchemy, falls nötig
if db_connection_str and db_connection_str.startswith("postgres://"):
    db_connection_str = db_connection_str.replace("postgres://", "postgresql://", 1)

# Wir definieren, wie viele Reihen wir laden wollen. Hier z.B. 100.000 (oder wir können das LIMIT in SQL entfernen für alle).
engine = create_engine(db_connection_str)
sample_size = 150000

query = f"""
WITH CohortUsers AS (
    SELECT DISTINCT user_id 
    FROM sessions 
    WHERE session_start >= '2023-01-04'
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

df = pd.read_sql(query, engine)
print(f"Daten geladen: {df.shape[0]} Reihen und {df.shape[1]} Spalten gefunden!")


plt.figure(figsize=(10, 5))
sns.boxplot(x=df['page_clicks'])
plt.title('Outliers bei Page Clicks')
plt.show()


# --- Visualisierungen für df ---
print("\n--- Erstelle Visualisierungen für df ---")

# Abbildung 1: Verteilungs-Plots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
fig.suptitle('Verteilung der Session-Metriken', fontsize=16)

# Histogramm für Page Clicks
sns.histplot(df['page_clicks'], bins=20, kde=True, ax=axes[0, 0])
axes[0, 0].set_title('Verteilung der Page Clicks')
axes[0, 0].set_xlabel('Page Clicks')
axes[0, 0].set_ylabel('Anzahl der Sessions')

# Histogramm für gebuchte Nächte
sns.histplot(df['nights'], bins=10, kde=False, ax=axes[0, 1])
axes[0, 1].set_title('Verteilung der gebuchten Nächte')
axes[0, 1].set_xlabel('Nächte')
axes[0, 1].set_ylabel('Anzahl der Sessions')

# Histogramm für Flugpreis (Base Fare)
sns.histplot(df['base_fare_usd'].dropna(), bins=20, kde=True, ax=axes[1, 0])
axes[1, 0].set_title('Verteilung des Flugpreises (USD)')
axes[1, 0].set_xlabel('Flugpreis (USD)')
axes[1, 0].set_ylabel('Anzahl der Sessions')

# Histogramm für Hotelpreis pro Zimmer/Nacht
sns.histplot(df['hotel_per_room_usd'].dropna(), bins=20, kde=True, ax=axes[1, 1])
axes[1, 1].set_title('Verteilung von Hotelpreis pro Zimmer/Nacht (USD)')
axes[1, 1].set_xlabel('Hotelpreis (USD)')
axes[1, 1].set_ylabel('Anzahl der Sessions')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Abbildung 2: Kategorische Count-Plots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
fig.suptitle('Buchungs- und Rabatt-Status', fontsize=16)

# Count-Plot für Flug- und Hotelbuchungen
booked_df = df[['flight_booked', 'hotel_booked']].melt(var_name='Booking Type', value_name='Booked')
sns.countplot(x='Booking Type', hue='Booked', data=booked_df, ax=axes[0])
axes[0].set_title('Flug vs. Hotel gebucht')
axes[0].set_xlabel('Buchungstyp')
axes[0].set_ylabel('Anzahl')

# Count-Plot für Flug- und Hotelrabatte
discount_df = df[['flight_discount', 'hotel_discount']].melt(var_name='Discount Type', value_name='Applied')
sns.countplot(x='Discount Type', hue='Applied', data=discount_df, ax=axes[1])
axes[1].set_title('Flug vs. Hotel Rabatt angewendet')
axes[1].set_xlabel('Rabatttyp')
axes[1].set_ylabel('Anzahl')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Abbildung 3: Beziehungs-Plots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
fig.suptitle('Beziehungen in den Session-Daten', fontsize=16)

# Scatter-Plot: Page Clicks vs. Flugpreis
sns.scatterplot(x='page_clicks', y='base_fare_usd', data=df, ax=axes[0])
axes[0].set_title('Page Clicks vs. Flugpreis (USD)')
axes[0].set_xlabel('Page Clicks')
axes[0].set_ylabel('Flugpreis (USD)')

# Box-Plot: Flugpreis nach Buchungsstatus
sns.boxplot(x='flight_booked', y='base_fare_usd', data=df, ax=axes[1], showfliers=False)
axes[1].set_title('Flugpreis pro Buchungsstatus (Outlier ausgeblendet)')
axes[1].set_xlabel('Flug gebucht')
axes[1].set_ylabel('Flugpreis (USD)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()



# Ausreißer in 'base_fare_usd' & 'page_clicks' behandeln
# Negative Base Fares auf 0 beschränken
df['base_fare_usd'] = df['base_fare_usd'].apply(lambda x: max(0, x) if pd.notnull(x) else x)

# Extreme "page_clicks"-Werte am 99%-Perzentil "cappen"
percentile_99_clicks = df['page_clicks'].quantile(0.99)
print(f"Das 99te Perzentil der Page Clicks liegt bei {percentile_99_clicks}. Alle Werte darüber werden nun geglättet.")

df['page_clicks'] = df['page_clicks'].clip(upper=percentile_99_clicks)


os.makedirs('../data', exist_ok=True)

# session_base.csv exportieren
session_base_cols = [
    'session_id', 'user_id', 'trip_id', 'session_start', 'session_end',
    'flight_discount', 'hotel_discount', 'flight_discount_amount', 
    'hotel_discount_amount', 'flight_booked', 'hotel_booked', 
    'page_clicks', 'cancellation'
]
session_base = df[session_base_cols].copy()
session_path = '../data/session_base.csv'
session_base.to_csv(session_path, index=False)

# not_canceled_trips.csv exportieren
not_canceled = df[
    (df['cancellation'] == False) & 
    (df['flight_booked'] | df['hotel_booked']) & 
    (df['trip_id'].notnull())
].copy()

# --- Zusätzliche Fehlerbehandlung für angetretene Reisen ---
print("Vor Fehlerbehebung in Reisendaten...")

# A. Vertauschte Check-in / Check-out Zeiten tauschen (Hotel)
not_canceled["check_in_time"] = pd.to_datetime(not_canceled["check_in_time"])
not_canceled["check_out_time"] = pd.to_datetime(not_canceled["check_out_time"])

mask_swapped = not_canceled["check_out_time"] < not_canceled["check_in_time"]
if mask_swapped.sum() > 0:
    print(f"- Korrigiere {mask_swapped.sum()} vertauschte Check-In/Check-Out Daten.")
    temp_checkin = not_canceled.loc[mask_swapped, "check_in_time"].copy()
    not_canceled.loc[mask_swapped, "check_in_time"] = not_canceled.loc[mask_swapped, "check_out_time"]
    not_canceled.loc[mask_swapped, "check_out_time"] = temp_checkin

# B. 0 Nächte trotz Hotelbuchung auf mindestens 1 setzen
mask_0_nights = (not_canceled["hotel_booked"] == True) & (not_canceled["nights"] == 0)
if mask_0_nights.sum() > 0:
    print(f"- Korrigiere {mask_0_nights.sum()} Hotelbuchungen mit 0 Nächten zu 1.")
    not_canceled.loc[mask_0_nights, "nights"] = 1

# C. 0 Sitze trotz Flugbuchung auf mindestens 1 setzen
mask_0_seats = (not_canceled["flight_booked"] == True) & (not_canceled["seats"] == 0)
if mask_0_seats.sum() > 0:
    print(f"- Korrigiere {mask_0_seats.sum()} Flugbuchungen mit 0 Sitzen zu 1.")
    not_canceled.loc[mask_0_seats, "seats"] = 1

not_canceled_path = '../data/not_canceled_trips.csv'
not_canceled.to_csv(not_canceled_path, index=False)

print(f"Gespeichert: {session_path} (Sessions/Interaktionen, {len(session_base)} Zeilen)")
print(f"Gespeichert: {not_canceled_path} (Nur angetretene Reisen, {len(not_canceled)} Zeilen)")

