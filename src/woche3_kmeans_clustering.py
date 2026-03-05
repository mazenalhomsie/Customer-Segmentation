import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_clustering():
    print("Starte Woche 3: K-Means Clustering...")
    
    input_path = 'data/user_base.csv'
    if not os.path.exists(input_path):
        print(f"Fehler: {input_path} existiert nicht.")
        return
        
    df = pd.read_csv(input_path)
    print(f"Lade {len(df)} Nutzer aus user_base.csv")
    
    # Feature Auswahl für das Clustering
    # Achtung: IDs (user_id) oder unskalierte Beträge dürfen nicht roh vermischt werden
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
    
    print(f"Verwendete Features: {features}")
    
    # Daten vorbereiten (falls es fehlende Werte geben sollte)
    X = df[features].fillna(0).copy()
    
    # 1. Feature Scaling (StandardScaler)
    # K-Means nutzt Distanzen, daher müssen alle Features die gleiche Skalierung (Mittelwert 0, Varianz 1) besitzen!
    print("Skaliere die Daten (StandardScaler)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. K-Means Clustering anwenden
    # Wir legen uns in diesem Skript auf k=4 fest (siehe Jupyter Notebook für die Evaluierung)
    k = 4
    print(f"Führe K-Means Clustering mit k={k} durch...")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Cluster-Zuordnung an den originalen DataFrame hängen
    df['cluster'] = clusters
    
    # 3. Speichern der Ergebnisse
    output_path = 'data/user_segments.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Woche 3: Clustering erfolgreich beendet.")
    print(f"[{len(df[df['cluster']==0])}] User in Cluster 0")
    print(f"[{len(df[df['cluster']==1])}] User in Cluster 1")
    print(f"[{len(df[df['cluster']==2])}] User in Cluster 2")
    print(f"[{len(df[df['cluster']==3])}] User in Cluster 3")
    print(f"Daten gespeichert unter: {output_path}")

if __name__ == "__main__":
    run_clustering()
