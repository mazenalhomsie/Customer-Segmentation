# Projektzusammenfassung: Mastery-Projekt TravelTide

**Autor:** Mazen
**Datum:** März 2026
**Thema:** Datengesteuerte Kundensegmentierung & Personalisierte Perks

---

## 📄 Executive Summary (Management-Zusammenfassung)

**Problemstellung:**
TravelTide verfügt über einen extrem umfangreichen Datensatz an Web-Traffic (Sessions) und Buchungen. Obwohl viele Nutzer auf der Plattform aktiv sind, konvertieren nicht alle zu zahlenden Kunden, und die Abwanderungsrate (Churn) bei bestimmten Gruppen ist hoch. Das Ziel dieses Projekts war es, durch Machine Learning unentdeckte Verhaltensmuster zu finden, um Kunden gezielt durch maßgeschneiderte Gutscheine (Perks) langfristig zu binden.

**Methodik:**
Es wurde eine automatisierte Datenpipeline (SQL & Python) entwickelt, die aus Millionen von Rohdaten eine verifizierte Business-Kohorte extrahiert (Nutzer nach dem 04. Jan 2023 mit >7 Sessions). Nach strikter Datenreinigung (GIGO-Prinzip, Ausreißer-Clipping nach IQR-Methode) wurden 14 hochkarätige Features pro Nutzer generiert (z. B. "Customer Lifetime Value", "Alter", "Business-Trip-Ratio"). Mittels **K-Means Clustering** (Unsupervised Learning) wurden diese Kunden anschließend datengetrieben in 4 Segmente gruppiert.

**Ergebnis & Handlungsempfehlung:**
Das Modell hat vier klare "Customer Personas" identifiziert, die nach einer gezielten Gutschein-Strategie verlangen:
1. **Cluster 0 (Young Window Shoppers - 21%):** Junge Singles (~32 J.), stöbern primär auf der Website. *Strategie: "Exclusive discounts" zur Erst-Konvertierung.*
2. **Cluster 1 (Frühbucher & Discount-Seeker - 10%):** Buchen sehr früh (Vorlauf 65 Tage), hohe Stornoquote (12%). *Strategie: "No cancellation fees" für mehr Buchungssicherheit.*
3. **Cluster 2 (Familienurlauber - 13%):** Längste Aufenthalte (6,6 Nächte), buchen sehr oft als Family-Trip. *Strategie: "1 night free hotel with flight".*
4. **Cluster 3 (Vielreisende & Business - 34%):** Buchen extrem spontan (Vorlauf ~9 Tage) und fliegen häufig alleine auf Business-Trip. *Strategie: "Free hotel meal" (Essen auf Firmenreisen).*
5. **Cluster 4 (Ältere verheiratete Urlauber - 22%):** Älteste Gruppe (~52 J.), meist verheiratet (93%), spontane Kurztrips ohne Kinder. *Strategie: "Free checked bag".*

Durch diese datengestützte Cluster-Zuweisung kann das Marketingbudget optimal allokiert und der Customer Lifetime Value (CLV) maximiert werden.

<div style="page-break-after: always;"></div>

---

## 📈 Detaillierter Bericht (Vertiefte Analyse)

### 1. Einleitung & Zielsetzung
In der modernen E-Commerce- und Tourismusbranche (Travel-Tech) reicht es heutzutage nicht mehr aus, allen Kunden pauschal denselben Newsletter oder denselben 5%-Gutschein zuzusenden ("Gießkannenprinzip"). Das Ziel dieses Mastery-Projekts war es deshalb, den Wertvorrat der eigenen PostgreSQL-Datenbank von "TravelTide" anzuzapfen und echte Kunden-Personas statistisch zu belegen. Jedem Kunden soll in Zukunft exakt der Incentive (Perk) angeboten werden, der seine persönliche Konvertierungswahrscheinlichkeit am stärksten erhöht.

### 2. Datenbasis & Preprocessing ("GIGO-Prinzip")
Das Projekt basierte auf vier stark verzweigten Tabellen (`users`, `sessions`, `flights`, `hotels`).
Gemäß dem GIGO-Prinzip ("Garbage In, Garbage Out") musste vor jeglicher Machine-Learning-Aktivität sichergestellt werden, dass die Datenbasis valide und fehlerfrei ist. Folgende Schritte wurden programmiert:
- **Datenbank-Extraktion & Kohorten-Filterung:** Um eine relevante Gruppe zu analysieren, wurden nur loyale und aktive Nutzer einbezogen (Anmeldung seit `Januar 2023` mit mehr als `7` Interaktionen).
- **Logik-Korrektur:** Buchungssystemfehler wurden automatisch via Python (`pandas`) korrigiert. Negative Hotel-Nächte wurden zu absoluten, positiven Zahlen transformiert. Vertauschte Check-In und Check-Out Daten wurden logisch gedreht.
- **Ausreißer-Behandlung (Clipping):** Extreme Web-Aktivitäten (User mit unnatürlich vielen `page_clicks`, potenziell Bots) wurden mithilfe der robusten IQR-Methode (Interquartile Range) abgefedert, da Distanzalgorithmen wie K-Means sonst stark verzerrt würden.
- **Validierung:** Mittels `pytest`-Framework wurde eine automatisierte Suite von Software-Tests (z.B. `test_negative_nights_fixed`) durchlaufen, um die Integrität nach der Säuberung mathematisch zu beweisen.

### 3. Feature Engineering
Da Machine Learning auf einer aggregierten User-Matrix operiert, wurden die bereinigten Transaktions- und Session-Daten auf "eine Zeile pro Nutzer" verdichtet. Es resultierten 14 tiefgreifende KPIs:
- **Ausgaben-Faktoren:** `total_spent`, `avg_spent_per_trip`
- **Reise-Eigenschaften:** `avg_nights_hotel`, `avg_booking_lead_time` (Tage zwischen Klick und Reise-Start).
- **Personas-Ratios:** `business_trip_ratio` (1 Sitz, <=1 Koffer, <=3 Nächte) und `family_trip_ratio` (>2 Sitze, >1 Zimmer).
- **Demografien:** `age` (Alter), `is_married` und `has_kids`.
- **Engagement-Faktoren:** `cancellation_rate`, `window_shopping_rate`, `discount_affinity`, `avg_page_clicks`, `total_sessions`.

Diese Features bilden das gesamte Profiling jedes Kundens datenpunktspezifisch ab.

### 4. Methodik: K-Means Clustering & Dimensionsreduktion (PCA)
Da die finalen Cluster im Voraus unbekannt waren, eignete sich unüberwachtes maschinelles Lernen (Unsupervised Machine Learning).
- **Skalierung:** Durch Anwendung des `StandardScaler` wurden finanzielle Beträge ($) und Prozentsätze (%) auf dieselbe Varianz (Mittelwert 0, Standardabweichung 1) nivelliert. Nur so kann verhindert werden, dass die reinen Dollar-Ausgaben alle anderen Kategorien bei der Distanzberechnung vernichten.
- **K-Means:** Unter Einsatz der Elbow-Methode und Betrachtung der Silhouette Scores wurde sich für `k=5` Cluster entschieden, was einen optimalen Kompromiss aus Homogenität und Marketing-Interpretierbarkeit darstellt.
- **Visualisierung (PCA):** Da Menschen keine 11 physikalischen Dimensionen sehen können, wurden die Features mittels *Principal Component Analysis (PCA)* auf eine 2D-Fläche projiziert, wodurch die visuelle Cluster-Trennung eindrucksvoll bestätigt wurde.

### 5. Identifizierte Customer Personas
Der Algorithmus gruppierte die TravelTide-Kohorte in folgende 5 trennscharfe Gruppen:

* **Cluster 0 (Young Window Shopper):** (1.252 User)
  Junge Singles (~32 J.), die massiv die Website durchstöbern (`window_shopping_rate` = 82%). Zeigen extrem geringe Totalausgaben (~1.230$), da sie nur bei absoluten Schnäppchen buchen.
* **Cluster 1 (Frühbucher & Discount-Seeker):** (610 User)
  Die extremste Gruppe in puncto Zukunftsplanung (Vorlauf: 65 Tage!). Sie weisen eine extrem hohe `cancellation_rate` (12%) auf (Die anderen Cluster liegen bei 0%). Wenn sie stornieren, nutzen sie stark unsere Gutscheine.
* **Cluster 2 (Premium Familienurlauber):** (759 User)
  Höchste `family_trip_ratio` (52%) und die längsten `avg_nights_hotel` (6,6 Nächte). Planen den großen Familienurlaub über TravelTide.
* **Cluster 3 (Business-Traveller & Vielreisende):** (2.023 User)
  Extrem hohe `business_trip_ratio` (58%) bei sehr kurzer Vorlaufzeit (9 Tage). Häufig alleinreisend und bringen massiven Lifetime Value ein.
* **Cluster 4 (Ältere verheiratete Urlauber):** (1.354 User)
  Älteste Gruppe (~52 Jahre), extrem oft verheiratet (93%). Buchen spontan für Kurztrips (oft zu zweit), reagieren gut auf Extras.

### 6. Fazit & Handlungsplan für Marketing
Durch die datengetriebene Cluster-Analyse wurde bewiesen, dass Kunden bei TravelTide nicht uniform agieren. Statt des Gießkannenprinzips lautet die klare Data-Science-Empfehlung für die Implementierung der neuen Gutschein-Mechanik (Perks) wie folgt:

* **Fokus Cluster 0 (Conversion steigern):** Um den Pool aus reinen "Guckern" zahlungspflichtig zu machen, erhalten sie den Perk **"Exclusive discounts"**.
* **Fokus Cluster 1 (Customer Success sichern):** Um Abbrüche trotz langer Frühbucher-Phasen zu verhindern, erhalten sie den Perk **"No cancellation fees"**.
* **Fokus Cluster 2 (Familien entlasten):** Großfamilien erhalten eine erlassene Hotel-Nacht (**"1 night free hotel with flight"**). Dies lindert den finanziellen Druck langer Aufenthalte.
* **Fokus Cluster 3 (Business-Loyalität):** Geschäftsreisende erhalten ein **"Free hotel meal"**. Dies stiftet persönlichen Mehrwert auf Business-Trips.
* **Fokus Cluster 4 (Best Ager Up-Selling):** Die ältere, verheiratete Generation bekommt das **"Free checked bag"**, um entspannt auf den spontanen Kurztrip zu zweit zu starten.

### 7. Erfolgsmessung (KPIs & Tracking für die nächsten Monate)
Um den ROI (Return on Investment) dieser Segmentierung messbar zu beweisen, sollten in den nächsten 3 bis 6 Monaten folgende Metriken durch A/B-Tests gemonitort werden:

1. **Conversion-Rate bei Cluster 0 (Young Window Shopper):** 
   - *KPI:* Prozentsatz der aktiven Sessions, die durch die aggressiven Rabatte nun tatsächlich zur Zahlung konvertieren.
   - *Erwartung:* Ein signifikanter Anstieg der Buchungsrate bei jungen Singles.
2. **Stornoquote bei Cluster 1 (Frühbucher):** 
   - *KPI:* Anzahl der Stornierungen dieser risikobehafteten Gruppe.
   - *Erwartung:* Ein klarer Rückgang unter die derzeitigen 12%, da das Sicherheitsnetz greift.
3. **Gutschein-Einlösequote (Redemption Rate) über alle Segmente:** 
   - *KPI:* Wie viele der dynamisch zugewiesenen Perks werden beim Checkout akzeptiert?
   - *Erwartung:* Eine drastisch höhere Akzeptanz als beim klassischen Gießkannen-Prinzip.
4. **Customer Lifetime Value (CLV) Erhaltung:** 
   - *KPI:* Der durchschnittliche Nettoumsatz pro Kunde (nach Abzug der Perk-Kosten).
   - *Erwartung:* Besonders Cluster 0 und 3 generieren loyal bedingt mehr Folge-Buchungen im System.
