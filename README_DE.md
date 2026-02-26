# Mastery-Projekt

## Projektüberblick
Dies ist das Abschlussprojekt "Mastery-Projekt" für den Data Science Kurs. Ziel ist es, eine reale, datengestützte Entscheidungsfindung zu simulieren. Du arbeitest mit einem Datensatz von **TravelTide**, einer Reisebuchungsplattform.

## Ziele
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

## Analyse starten
Öffne `notebooks/01_Initial_Exploration.ipynb`, um mit der ersten Analyse zu beginnen.
