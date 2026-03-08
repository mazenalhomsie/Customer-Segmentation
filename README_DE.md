# Mastery-Projekt

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green?logo=pandas&logoColor=white)

## Projektüberblick
Dies ist das Abschlussprojekt "Mastery-Projekt" für den Data Science Kurs. Ziel ist es, eine reale, datengestützte Entscheidungsfindung zu simulieren. Du arbeitest mit einem Datensatz von **TravelTide**, einer Reisebuchungsplattform.

## Projektziele (Project Objectives)
Das Hauptziel dieses Projekts ist der Aufbau eines datengesteuerten Kundensegmentierungsmodells, um zielgerichtete Gutscheine/Vergünstigungen zu verteilen. Durch die Analyse des Nutzerverhaltens und der Buchungsmuster wurden Features extrahiert und Unsupervised Machine Learning (K-Means) angewendet, um die Kunden in Segmente (Cluster) zu unterteilen.

## Hauptfunktionen (Key Features)
- **Automatisierte Datenpipeline:** Sicherer Import der Daten-Kohorte aus der PostgreSQL-Datenbank (via `.env`).
- **Data Cleaning & Preprocessing:** Automatische Behandlung von fehlerhaften Werten (negative Nächte, vertauschte Daten) und Outlier-Clipping (IQR-Methode).
- **Fortgeschrittenes Feature Engineering:** Erstellung von Raten und Metriken wie `cancellation_rate`, `window_shopping_rate`, `business_trip_ratio` und `total_spent`.
- **Kundensegmentierung (ML):** Unsupervised Machine Learning per K-Means Clustering. Evaluiert mittels Silhouette-Scores und visualisiert über PCA (Principal Component Analysis).
- **Interaktive Notebooks:** Modulare Jupyter-Notebooks, die jeden Schritt von der EDA bis zur ML-Segmentierung dokumentieren.

## Techniken & Tools (Techniques & Tools)
- **Programmiersprache:** Python 3.8+
- **Datenbank:** PostgreSQL, SQLAlchemy, `psycopg2-binary`
- **Datenverarbeitung:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (K-Means Clustering, PCA, StandardScaler)
- **Datenvisualisierung:** Matplotlib, Seaborn
- **Arbeitsumgebung:** Jupyter Notebooks, `python-dotenv`

## Projektphasen
1. **Woche 1: Projekt-Exploration**
   - Datensatz und geschäftlichen Kontext verstehen.
   - Hauptziele und Anforderungen definieren.
   - Explorative Datenanalyse (EDA).
2. **Woche 2: Feature Engineering & Kundensegmentierung**
   - Datenqualität verbessern.
   - Metriken entwickeln (z.B. Customer Lifetime Value, Churn Probability).
3. **Woche 3: Erkenntnisse und Strategie entwickeln**
   - Kundensegmentierung (Clustering).
   - Datengetriebene Empfehlungen.
4. **Woche 4: Präsentation deiner Ergebnisse**
   - Finale Strategie präsentieren.

## Datenstruktur
Die Daten stammen aus einer PostgreSQL-Datenbank.
Es gibt 4 Haupttabellen:

### 1. `users` (Nutzerdaten)
- `user_id`: Eindeutige ID
- `birthdate`, `gender`, `married`, `has_children`
- `home_country`, `home_city`, `home_airport`
- `sign_up_date`

### 2. `sessions` (Sitzungsdaten / Web-Traffic)
- `session_id`: Eindeutige Session ID
- `user_id`: Fremdschlüssel zu `users`
- `trip_id`: ID der Reise (falls gebucht)
- `session_start`, `session_end`
- `flight_booked`, `hotel_booked`, `cancellation`
- `flight_discount`, `hotel_discount`
- `page_clicks`

### 3. `flights` (Flugdaten)
- `trip_id`: Eindeutige Reise ID
- `origin_airport`, `destination_airport`
- `departure_time`, `return_time`
- `base_fare_usd`: Preis
- `trip_airline`

### 4. `hotels` (Hoteldaten)
- `trip_id`: Eindeutige Reise ID
- `hotel_name`
- `nights`, `rooms`
- `check_in_time`, `check_out_time`
- `hotel_per_room_usd`: Preis pro Nacht/Zimmer

## Setup & Installation

### Voraussetzungen
- Python 3.8+
- Jupyter Notebook
- PostgreSQL (für direkten DB-Zugriff) oder CSV-Dateien

### Installation der Abhängigkeiten
```bash
pip install -r requirements.txt
```

### Daten laden
Um die Daten zu laden, verwende die Skripte in `src/`:

- **Sample Daten (10k Zeilen pro Tabelle):**
  ```bash
  python src/fetch_sample_data.py
  ```
  Die Daten werden im Ordner `data/` als CSV gespeichert.

- **Vollständige Daten:**
  (Skript `src/fetch_data.py` - Achtung: Datensatz ist groß > 5 Mio Zeilen)

## Projektstruktur
```text
Customer-Segmentation/
├── data/                  # Generierte CSV Datensätze (ignoriert durch git)
├── notebooks/             # Jupyter Notebooks für EDA, Feature Eng. und ML
├── presentation/          # Projektpräsentation in Deutsch (Slides)
├── src/                   # Python Skripte für Datenpipelines
├── .env                   # Umgebungsvariablen für die Datenbank
├── plann.md               # Wöchentliche Roadmap und Aufgabenliste
├── requirements.txt       # Python Abhängigkeiten
├── README.md              # Dokumentation (Englisch)
└── README_DE.md           # Dokumentation (Deutsch)
```

## Preprocessing & GIGO Prinzip
> **"Garbage In, Garbage Out" (GIGO)**
> Die Qualität der Segmentierung ist nur so gut wie die Datenbasis. Um zu verhindern, dass fehlerhafte Einträge (Ausreißer, Buchungsfehler) die Ergebnisse des Machine Learnings (K-Means) zerstören, wurde großer Wert auf eine rigorose Datenreinigung und ein automatisiertes Testing (`pytest`) gelegt.

Das Skript `src/woche1_preprocessing.py` übernimmt das Data Cleaning und filtert gleichzeitig die Kohorte (Nutzer ab 04. Jan 2023 mit > 7 Sessions):
- **Negative Nächte (`nights`):** Da Aufenthalte nicht negativ sein können, wandeln wir diese per SQL (`ABS`) in positive, absolute Werte um.
- **Preisausreißer (`base_fare_usd`):** Falls fehlerhafte negative Flugpreise existieren, werden diese auf 0 gesetzt.
- **Extreme Interaktionen (`page_clicks`):** Um logische Ausreißer abzufangen, werden die Ticketkäufe / Klicks mit der IQR-Methode (Interquartile Range) beschnitten ("Clipping").

```bash
python src/woche1_preprocessing.py
```
Durch das Skript werden die bereinigten Datensätze `session_base.csv` und `not_canceled_trips.csv` im Ordner `data/` abgelegt.

## Identifizierte Kundensegmente (K-Means Clustering)
Das K-Means Clustering (`woche3_kmeans_clustering.py`) teilt die User nach 14 verhaltensbasierten und demografischen Features in diese Personas ein:
1. **Cluster 0 (Young Window Shopper):** Junge Singles (~32 Jahre), stöbern primär auf der Website (Window Shopping: 82%) mit niedrigsten Ausgaben (~$1230).
2. **Cluster 1 (Frühbucher & Discount-Jäger):** Buchen >2 Monate (65 Tage) im Voraus. Höchste Storno-Quote (12%).
3. **Cluster 2 (Familienurlauber):** Längste Aufenthalte (6,6 Nächte) und sehr hohe Family-Trip Ratio (52%).
4. **Cluster 3 (Vielreisende & Business-Traveller):** Buchen spontan (Lead Time ~9 Tage), sehr hohe Business-Trip Ratio (58%). 
5. **Cluster 4 (Ältere Verheiratete Urlauber):** Älteste Gruppe (~52 Jahre), fast alle verheiratet (93%), buchen spontan und mit moderatem Budget.

## Analyse starten
Öffne `notebooks/01_Woche_1_Exploration_und_Preprocessing.ipynb`, um mit der ersten Analyse zu beginnen.
