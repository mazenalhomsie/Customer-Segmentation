# Mastery Project

## Project Overview
This is the final capstone project "Mastery Project" for the Data Science course. The goal is to simulate real-world data-driven decision making. You will be working with a dataset from **TravelTide**, a travel booking platform.

## Objectives
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

## Start Analysis
Open `notebooks/01_Initial_Exploration.ipynb` to start with the initial analysis.

---
*For German documentation, see [README_DE.md](README_DE.md).*
