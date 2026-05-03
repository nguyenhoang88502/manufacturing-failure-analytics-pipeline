# CO4031 BTL - Manufacturing Data Warehouse System

## Project Overview
Academic data warehouse project (CO4031 BTL) implementing a full ETL pipeline and star schema for manufacturing machine failure analysis.

## Architecture

### Data Flow
```
Raw CSV (ai4i2020.csv)
  → Data Cleaning & Feature Engineering (run_etl.py)
  → Staging DB (staging.machine_data)
  → Star Schema DW (dw.* tables)
  → OLAP Analysis Queries
```

### Database Schema
- **staging.machine_data** - Cleaned staging area
- **dw.dim_date** - Date dimension (365 rows for 2023)
- **dw.dim_product** - Product quality dimension
- **dw.dim_failure_type** - Failure type dimension (6 types)
- **dw.dim_machine_condition** - Machine condition dimension (4 levels)
- **dw.fact_machine_operations** - Central fact table (~9,800+ rows)

### Directory Structure
```
run_etl.py               - Main ETL pipeline (run this)
data/
  raw/
    ai4i2020.csv         - Original AI4I 2020 Predictive Maintenance dataset
    01_exploration.py    - Original exploration script (Windows paths)
  cleaned/
    machine_data_cleaned.csv - Cleaned dataset output
    eda_distributions.png    - Feature distribution plots
    correlation_heatmap.png  - Feature correlation heatmap
etl/
  staging.sql            - Staging schema DDL
  machine_etl.ktr        - Kettle/PDI ETL transformation
  02 _load_to_dw.py      - Original load script (Windows paths)
dw/
  01_create_star_schema.sql - Star schema DDL
  02_populate_star.py       - Original populate script (Windows paths)
  OLAP *.sql / *.csv        - OLAP query results
```

## Running the Pipeline
The workflow runs `python run_etl.py` which executes all 5 steps:
1. Load & clean raw CSV data
2. Feature engineering (K→C conversion, power calc, failure labels)
3. Load cleaned data to staging PostgreSQL table
4. Populate star schema from staging
5. Run OLAP analysis queries and print results

## Environment
- **Language**: Python 3.x
- **Database**: Replit PostgreSQL (env vars: DATABASE_URL, PGHOST, etc.)
- **Key packages**: pandas, sqlalchemy, psycopg2-binary, numpy, matplotlib, seaborn

## Dataset
AI4I 2020 Predictive Maintenance Dataset (~10,000 manufacturing operation records)
- Features: air temp, process temp, rotational speed, torque, tool wear
- Target: machine failure and failure type classification
