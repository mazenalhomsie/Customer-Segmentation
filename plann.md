# To-Do Liste

## Woche 1
- [x] Verbinden mit der SQL Datenbank
- [x] Überblick verschaffen über Spalten und Tabellen
- [x] Cohort Filtering Export auf CSV für Python
- [x] Ausreißer erkennen und behandeln
- [x] Negative Nächte erkennen und behandeln
- [x] Etwaiges Preprocessing
- [x] Verstehen wie Interaktionen, Buchungen und Stornierungen zusammenhängen
- [x] Angetretene Reisen (not canceled trips) erkennen und abspeichern
- [x] Am ende ein session_base.csv und ein not_canceled_trips.csv

## Woche 2
- [x] Aggregieren auf User-Level (jeder User hat mehrere Sessions)
- [x] Features überlegen die man pro User abbilden (zB Anzahl der Reisen pro Kunde, Durchschnittliche Ausgaben pro Kunde, …)
- [x] Annahmen Treffen über den Kunden und Spalten verbinden (zB Businessreise JA/NEIN -> fliegt während Woche, fliegt alleine, fliegt mit wenig bis gar keinem Aufgabegepäck)
- [x] Features überlegen für base_session.csv -> zB window shopping, Stornos
- [x] Features überlegen für Reisen -> zB durchschnittliche Nächte im Hotel
- [x] Am ende user_base.csv
- [x] Überlegen wie wir weiter segmentieren (ML oder manuell)

## Woche 3 🔄
- [x] Entscheiden ob Clustering Ansatz oder manuell -> **Entscheidung: Machine Learning (K-Means Clustering)**
- [ ] ~~Für manuell features entscheiden die einen Gutschein ausmachen~~ (Hinfällig, da ML Ansatz)
- [x] Daten vorbereiten für PCA (Scaling & Dimensionality Reduction)
- [x] Daten Clustern mit K Means und Silhouette Scores
- [x] Cluster interpretieren und analysieren
- [x] Perks zuweisen zu jedem Cluster, gegebenenfalls Perks erfinden oder mehrmals zuweisen
- [x] Am ende haben wir unsere Customer Segmentation, eine Zuweisung welcher Kunder (user_id) zu welchem Segment gehört und welchen Gutschein er/sie bekommt

## Woche 4
- [ ] Report schreiben und finalisieren (Abstract und detaillierter Ablauf)
- [ ] Präsentation vorbereiten
- [ ] GitHub Repo erstellen und Code-Fragmente organisieren
- [ ] Ordnerstruktur für das Projekt finalisieren und auf GitHub hochladen
- [ ] ReadMe file schreiben (wie führe ich den Code aus? In welcher Reihenfolge?, mehr dazu in der Learning Journey)
- [ ] Vor der Präsentation das Projekt auf Codio abgeben
- [ ] Präsentieren nur möglich wenn zuvor abgegeben wurde
- [ ] Ende
