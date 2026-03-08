import pandas as pd
import numpy as np

features = [
    'total_sessions', 
    'cancellation_rate', 
    'window_shopping_rate',
    'discount_affinity',
    'avg_page_clicks',
    'total_trips', 
    'total_spent',
    'avg_nights_hotel',
    'avg_booking_lead_time',
    'business_trip_ratio', 
    'family_trip_ratio'
]

df = pd.read_csv('data/user_segments.csv')

# Cluster Analysis
cluster_analysis = df.groupby('cluster')[features].mean().round(2)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("--- Durchschnittswerte pro Segment ---\n")
    f.write(cluster_analysis.to_string())
    f.write("\n\n--- Anzahl der Nutzer pro Cluster ---\n")
    f.write(df['cluster'].value_counts().sort_index().to_string())
