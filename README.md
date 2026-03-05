# Mastery Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green?logo=pandas&logoColor=white)

## Project Overview
This is the final capstone project "Mastery Project" for the Data Science course. The goal is to simulate real-world data-driven decision making. You will be working with a dataset from **TravelTide**, a travel booking platform.

## Project Objectives
The primary objective of this project is to build a data-driven customer segmentation model to distribute targeted perks (vouchers/discounts). By analyzing user behavior and booking patterns, we engineered features and applied unsupervised machine learning to cluster customers into actionable segments.

## Key Features
- **Automated Data Pipeline:** Secure data extraction of the chosen cohort from a PostgreSQL database.
- **Data Cleaning & Preprocessing:** Automatic handling of invalid entries (negative nights, swapped dates) and outlier capping (IQR Method).
- **Advanced Feature Engineering:** Creation of user-centric features like `cancellation_rate`, `window_shopping_rate`, `business_trip_ratio`, and `total_spent`.
- **Customer Segmentation (ML):** Unsupervised Machine Learning using K-Means Clustering, evaluated with Silhouette Scores, and visualized via PCA.
- **Interactive Notebooks:** Modular Jupyter Notebooks documenting every step from EDA to ML.

## Techniques & Tools
- **Language:** Python 3.8+
- **Database:** PostgreSQL, SQLAlchemy, `psycopg2-binary`
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (K-Means Clustering, PCA, StandardScaler)
- **Data Visualization:** Matplotlib, Seaborn
- **Environment:** Jupyter Notebooks, `python-dotenv`

## Project Phases
1. **Week 1: Project Exploration**
   - Understand the dataset and business context.
   - Define main goals and requirements.
   - Exploratory Data Analysis (EDA).
2. **Week 2: Feature Engineering & Customer Segmentation**
   - Improve data quality.
   - Develop metrics (e.g., Customer Lifetime Value, Churn Probability).
3. **Week 3: Insights and Strategy Development**
   - Customer Segmentation (Clustering).
   - Data-driven recommendations.
4. **Week 4: Presentation of Results**
   - Present final strategy.

## Data Structure
The data comes from a PostgreSQL database.
There are 4 main tables:

### 1. `users` (User Data)
- `user_id`: Unique ID
- `birthdate`, `gender`, `married`, `has_children`
- `home_country`, `home_city`, `home_airport`
- `sign_up_date`

### 2. `sessions` (Session Data / Web Traffic)
- `session_id`: Unique Session ID
- `user_id`: Foreign Key to `users`
- `trip_id`: ID of the trip (if booked)
- `session_start`, `session_end`
- `flight_booked`, `hotel_booked`, `cancellation`
- `flight_discount`, `hotel_discount`
- `page_clicks`

### 3. `flights` (Flight Data)
- `trip_id`: Unique Trip ID
- `origin_airport`, `destination_airport`
- `departure_time`, `return_time`
- `base_fare_usd`: Price
- `trip_airline`

### 4. `hotels` (Hotel Data)
- `trip_id`: Unique Trip ID
- `hotel_name`
- `nights`, `rooms`
- `check_in_time`, `check_out_time`
- `hotel_per_room_usd`: Price per night/room

## Setup & Installation

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- PostgreSQL (for direct DB access) or CSV files

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Load Data
To load the data, use the scripts in `src/`:

- **Sample Data (10k rows per table):**
  ```bash
  python src/fetch_sample_data.py
  ```
  The data will be saved as CSV in the `data/` folder.

- **Full Data:**
  (Script `src/fetch_data.py` - Note: Dataset is large > 5 million rows)

## Project Structure
```text
Customer-Segmentation/
├── data/                  # Generated CSV datasets (ignored by git)
├── notebooks/             # Jupyter Notebooks for EDA, Engineering, and ML
├── presentation/          # Project presentation slides (German)
├── src/                   # Python scripts for data pipelines and modeling
├── .env                   # Environment variables for database credentials
├── plann.md               # Weekly project roadmap and checklist
├── requirements.txt       # Python package dependencies
├── README.md              # Documentation (English)
└── README_DE.md           # Documentation (German)
```

## Preprocessing & GIGO Principle
> **"Garbage In, Garbage Out" (GIGO)**
> The quality of segmentation is only as good as the data foundation. To prevent faulty entries (outliers, booking errors) from destroying our Machine Learning (K-Means) results, we placed a heavy emphasis on rigorous data cleaning and automated testing (`pytest`).

The script `src/woche1_preprocessing.py` manages the data cleaning and cohort filtering (Users from Jan 4, 2023 with > 7 sessions):
- **Negative Nights (`nights`):** Since stays cannot be negative, we use SQL (`ABS`) to convert them to positive absolute values.
- **Price Outliers (`base_fare_usd`):** Any erroneous negative flight prices, if they exist, are set to 0.
- **Extreme Interactions (`page_clicks`):** To manage large outliers, the page clicks are capped using the Interquartile Range (IQR) method.

```bash
python src/woche1_preprocessing.py
```
This script extracts the cleaned `session_base.csv` and `not_canceled_trips.csv` datasets to the `data/` folder.

## Identified Customer Segments (K-Means Clustering)
The K-Means Clustering (`woche3_kmeans_clustering.py`) categorizes users into these personas based on 11 behavioral features:
1. **Cluster 0 (Frequent & Business Travelers):** Book extremely spontaneously (Lead Time ~9 days), very high Business-Trip Ratio (61%).
2. **Cluster 1 (Window Shopper & Budget Explorer):** Almost exclusively on the website to browse (Window Shopping: 84%). Lowest spending (Lifetime Value ~$990).
3. **Cluster 2 (Family Vacationers):** Longest stays (6.5 nights) and very high Family-Trip Ratio (40%). 
4. **Cluster 3 (Early Birds & Discount Seekers):** Book >2 months (65 days) in advance. Highest cancellation rate (12%) and strong response to discounts.

## Start Analysis
Open `notebooks/01_Woche_1_Exploration_und_Preprocessing.ipynb` to start with the initial analysis.

---
*For German documentation, see [README_DE.md](README_DE.md).*
