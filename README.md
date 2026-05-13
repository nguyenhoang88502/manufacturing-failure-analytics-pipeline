# Manufacturing Failure Analysis Dashboard

This project is a complete data analysis system for manufacturing machine failures.

In simple terms: it starts with a CSV file of machine operation records, cleans that data, organizes it into a database structure that is easy to analyze, creates summary result files, shows those results in an interactive dashboard, and also includes an optional machine learning model that tries to predict whether a machine operation will fail.

The project was built for CO4031 and uses the AI4I 2020 predictive maintenance dataset.

## Table of Contents

- [Plain English Summary](#plain-english-summary)
- [What This Project Can Answer](#what-this-project-can-answer)
- [How The Whole System Works](#how-the-whole-system-works)
- [Repository Structure](#repository-structure)
- [Main Files](#main-files)
- [Requirements](#requirements)
- [Quick Start: Run The Dashboard](#quick-start-run-the-dashboard)
- [Recreate The Project From Scratch](#recreate-the-project-from-scratch)
- [Dataset Explanation](#dataset-explanation)
- [Data Cleaning And Feature Engineering](#data-cleaning-and-feature-engineering)
- [Database And Star Schema](#database-and-star-schema)
- [OLAP Analysis Files](#olap-analysis-files)
- [Dashboard Explanation](#dashboard-explanation)
- [Machine Learning Explanation](#machine-learning-explanation)
- [Every Python File Explained](#every-python-file-explained)
- [Every Important Non-Python File Explained](#every-important-non-python-file-explained)
- [Common Problems And Fixes](#common-problems-and-fixes)
- [Recommended Presentation Flow](#recommended-presentation-flow)

## Plain English Summary

Factories use machines to make products. Each machine operation produces measurements such as:

- air temperature
- process temperature
- rotational speed
- torque
- tool wear
- product quality type
- whether the machine failed
- what kind of failure happened

Raw machine data is not very useful by itself. It is just rows and columns. This project turns that raw data into useful information.

The project does five main things:

1. Reads the raw manufacturing CSV file.
2. Cleans and prepares the data so the values are consistent.
3. Loads the data into PostgreSQL using a data warehouse design.
4. Creates OLAP summary CSV files for business analysis.
5. Displays the analysis in a Streamlit dashboard.

There is also a machine learning script that trains an XGBoost model to predict whether a machine operation is likely to fail.

## What This Project Can Answer

The dashboard and warehouse help answer questions like:

- How many machine operations are in the data?
- How many operations ended in machine failure?
- What percentage of operations failed?
- Which failure type happened most often?
- Does low-quality product type fail more often than high-quality product type?
- Does tool wear increase the chance of failure?
- Which machine condition is most risky?
- Which months have more failures?
- Can we train a model to predict machine failure from sensor values?

## How The Whole System Works

The full workflow looks like this:

```text
Raw CSV data
    |
    v
Clean and transform data with Python
    |
    v
Save cleaned CSV
    |
    v
Load cleaned data into PostgreSQL staging table
    |
    v
Populate data warehouse star schema
    |
    v
Run OLAP SQL queries
    |
    v
Export OLAP results as CSV files
    |
    v
Show CSV results in Streamlit dashboard
```

The machine learning workflow uses the cleaned CSV:

```text
Cleaned CSV
    |
    v
Train/test split
    |
    v
Balance failure and non-failure examples with SMOTE
    |
    v
Scale numeric features
    |
    v
Train XGBoost model
    |
    v
Save model, scaler, evaluation plots, and SHAP explanation plot
```

## Repository Structure

```text
.
|-- app.py
|-- main.py
|-- run_etl.py
|-- pyproject.toml
|-- README.md
|
|-- .streamlit/
|   `-- config.toml
|
|-- data/
|   |-- raw/
|   |   |-- ai4i2020.csv
|   |   `-- 01_exploration.py
|   `-- cleaned/
|       |-- machine_data_cleaned.csv
|       |-- eda_distributions.png
|       `-- correlation_heatmap.png
|
|-- etl/
|   |-- staging.sql
|   |-- 02 _load_to_dw.py
|   `-- machine_etl.ktr
|
|-- dw/
|   |-- 01_create_star_schema.sql
|   |-- 02_populate_star.py
|   |-- OLAP Failure Distribution by Failure Type.sql
|   |-- OLAP Failure Distribution by Failure Type.csv
|   |-- OLAP Failure Rate by Product Quality Type.sql
|   |-- OLAP Failure Rate by Product Quality Type.csv
|   |-- OLAP Machine Condition vs Failure Rate.sql
|   |-- OLAP Machine Condition vs Failure Rate.csv
|   |-- OLAP Monthly Failure Trend.sql
|   |-- OLAP Monthly Failure Trend.csv
|   `-- ETL & DW & OLAP.docx
|
|-- ml/
|   |-- xgboost_failure_prediction.py
|   |-- xgboost_model.pkl
|   |-- scaler.pkl
|   `-- plots/
|       |-- model_evaluation.png
|       `-- shap_summary.png
|
|-- picture/
|   |-- 01_kpi_cards.jpg
|   |-- 01_overview_top.jpg
|   |-- 02_failure_distribution_bar.jpg
|   |-- 03_monthly_trend_line.jpg
|   |-- 04_machine_condition_scatter.jpg
|   |-- 05_product_quality_bar.jpg
|   |-- 06_data_tables.jpg
|   |-- 07_sidebar_filters.jpg
|   `-- 08_full_dashboard_composite.jpg
|
`-- report/
    `-- report and project images
```

## Main Files

| File or folder | Purpose |
| --- | --- |
| `app.py` | The Streamlit dashboard. This is the main file to run if you only want to view the dashboard. |
| `run_etl.py` | The main end-to-end Python ETL script. It cleans data, loads staging, populates the warehouse, and prints OLAP summaries. |
| `data/raw/ai4i2020.csv` | Original raw dataset. |
| `data/cleaned/machine_data_cleaned.csv` | Cleaned dataset created from the raw dataset. |
| `dw/01_create_star_schema.sql` | SQL script that creates the data warehouse schema and dimension tables. |
| `dw/*.sql` | OLAP query scripts. |
| `dw/*.csv` | Exported OLAP results used directly by the dashboard. |
| `ml/xgboost_failure_prediction.py` | Optional machine learning training script. |
| `pyproject.toml` | Python project metadata and core dependencies. |
| `.streamlit/config.toml` | Streamlit server settings. |

## Requirements

You need Python 3.11 or newer.

For the dashboard only, you need:

- Python
- pandas
- Streamlit
- Plotly

For the full ETL and database rebuild, you also need:

- PostgreSQL
- SQLAlchemy
- psycopg2-binary

For machine learning, you also need:

- scikit-learn
- imbalanced-learn
- xgboost
- shap
- matplotlib
- seaborn

The core dependencies in `pyproject.toml` are:

```toml
dependencies = [
    "matplotlib>=3.10.9",
    "numpy>=2.4.4",
    "pandas>=3.0.2",
    "playwright>=1.59.0",
    "plotly>=6.7.0",
    "psycopg2-binary>=2.9.12",
    "seaborn>=0.13.2",
    "sqlalchemy>=2.0.49",
    "streamlit>=1.57.0",
]
```

Important note: the machine learning script imports packages that are not currently listed in `pyproject.toml`: `scikit-learn`, `imbalanced-learn`, `xgboost`, and `shap`. Install them separately if you want to run the ML script.

## Quick Start: Run The Dashboard

Use this if you only want to open the dashboard.

### 1. Open a terminal in the project folder

On this machine, the project folder is:

```powershell
c:\Users\nguyenhoang88502\Documents\GitHub\co4031_project
```

In PowerShell:

```powershell
cd c:\Users\nguyenhoang88502\Documents\GitHub\co4031_project
```

### 2. Create a virtual environment

A virtual environment is a private Python environment for this project. It keeps this project's libraries separate from other Python projects.

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -e .
```

### 5. Run the dashboard

```powershell
streamlit run app.py
```

The Streamlit config uses:

```text
address = "0.0.0.0"
port = 5000
```

Open this in your browser:

```text
http://localhost:5000
```

If Streamlit prints a different URL, use the URL printed in the terminal.

## Recreate The Project From Scratch

This section explains how to rebuild the whole project from the raw data.

### Step 1: Start with the raw dataset

Place the original AI4I 2020 CSV file here:

```text
data/raw/ai4i2020.csv
```

The raw file should have columns like:

```text
UDI
Product ID
Type
Air temperature [K]
Process temperature [K]
Rotational speed [rpm]
Torque [Nm]
Tool wear [min]
Machine failure
TWF
HDF
PWF
OSF
RNF
```

### Step 2: Install Python dependencies

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

For machine learning, also run:

```powershell
pip install scikit-learn imbalanced-learn xgboost shap
```

### Step 3: Create the PostgreSQL database

Install PostgreSQL if it is not already installed.

Create a database named:

```text
co4031_dw
```

One way to do it with `createdb`:

```powershell
createdb -U postgres co4031_dw
```

If your PostgreSQL username is not `postgres`, replace it with your username.

### Step 4: Create the warehouse tables

Run the star schema SQL:

```powershell
psql -U postgres -d co4031_dw -f "dw\01_create_star_schema.sql"
```

This creates:

- `dw.dim_date`
- `dw.dim_product`
- `dw.dim_failure_type`
- `dw.dim_machine_condition`
- `dw.fact_machine_operations`

### Step 5: Set the database connection for `run_etl.py`

`run_etl.py` reads the database connection from an environment variable called `DATABASE_URL`.

In PowerShell:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/co4031_dw"
```

Replace `YOUR_PASSWORD` with your real PostgreSQL password.

### Step 6: Run the full ETL script

```powershell
python run_etl.py
```

This script does these jobs:

1. Reads `data/raw/ai4i2020.csv`.
2. Cleans the data.
3. Creates derived features.
4. Saves `data/cleaned/machine_data_cleaned.csv`.
5. Creates and fills `staging.machine_data`.
6. Fills the data warehouse fact and dimension tables.
7. Prints OLAP summaries in the terminal.

Important: `run_etl.py` expects the `dw` schema and dimension tables to already exist, so run `dw/01_create_star_schema.sql` first.

### Step 7: Export OLAP CSV files

The dashboard reads CSV files from the `dw` folder. The four required CSV files are:

```text
dw/OLAP Failure Distribution by Failure Type.csv
dw/OLAP Failure Rate by Product Quality Type.csv
dw/OLAP Machine Condition vs Failure Rate.csv
dw/OLAP Monthly Failure Trend.csv
```

To recreate them:

1. Open PostgreSQL, pgAdmin, DBeaver, or another SQL client.
2. Run each SQL file in the `dw` folder whose name starts with `OLAP`.
3. Export each result as CSV.
4. Save each CSV using the exact filenames above.

The dashboard expects those exact column names and filenames.

### Step 8: Run the dashboard

```powershell
streamlit run app.py
```

### Step 9: Optionally train the ML model

Make sure this file exists:

```text
data/cleaned/machine_data_cleaned.csv
```

Then run:

```powershell
python ml\xgboost_failure_prediction.py
```

The script creates:

```text
ml/xgboost_model.pkl
ml/scaler.pkl
ml/plots/model_evaluation.png
ml/plots/shap_summary.png
```

## Dataset Explanation

The raw dataset is the AI4I 2020 predictive maintenance dataset. It contains 10,000 machine operation rows.

Each row means one recorded machine operation.

Important raw columns:

| Column | Simple meaning |
| --- | --- |
| `UDI` | Unique row ID. Think of it as the record number. |
| `Product ID` | Product identifier. |
| `Type` | Product quality group. `L` means low quality, `M` means medium quality, `H` means high quality. |
| `Air temperature [K]` | Air temperature in Kelvin. |
| `Process temperature [K]` | Machine process temperature in Kelvin. |
| `Rotational speed [rpm]` | How fast the machine rotates. RPM means rotations per minute. |
| `Torque [Nm]` | Twisting force. Higher torque means the machine is working harder. |
| `Tool wear [min]` | How long the tool has been used. Higher values mean the tool is more worn. |
| `Machine failure` | `1` if the machine failed, `0` if it did not. |
| `TWF` | Tool Wear Failure flag. |
| `HDF` | Heat Dissipation Failure flag. |
| `PWF` | Power Failure flag. |
| `OSF` | Overstrain Failure flag. |
| `RNF` | Random Failure flag. |

Failure flags are binary:

- `0` means no
- `1` means yes

For example, if `HDF = 1`, that row had a heat dissipation failure.

## Data Cleaning And Feature Engineering

Raw data usually needs cleaning before analysis. This project does that in `run_etl.py` and `data/raw/01_exploration.py`.

### Cleaning steps

The cleaning process:

1. Reads the raw CSV.
2. Checks the number of rows and columns.
3. Checks for missing values.
4. Checks for duplicate rows.
5. Removes duplicate rows.
6. Fills missing numeric values with the median value of that column.
7. Removes physically impossible values, such as negative torque.
8. Removes extreme outliers from rotational speed and torque using the IQR method.

### What IQR outlier removal means

IQR means interquartile range.

A simple explanation:

- Sort the values from smallest to largest.
- Find the middle range where most values live.
- Values that are extremely far outside that range are treated as outliers.

This project uses a wide IQR factor of `3.0`, so it only removes very extreme values.

### New columns created

The scripts create these derived columns:

| New column | How it is created | Why it matters |
| --- | --- | --- |
| `air_temp_c` | `Air temperature [K] - 273.15` | Converts Kelvin to Celsius, which is easier to understand. |
| `process_temp_c` | `Process temperature [K] - 273.15` | Converts process temperature to Celsius. |
| `temp_differential_c` | `process_temp_c - air_temp_c` | Shows how much hotter the machine process is than the surrounding air. |
| `power_w` | `Torque * (2 * pi * RPM / 60)` | Estimates mechanical power in watts. |
| `type_encoded` | `L = 0`, `M = 1`, `H = 2` | Converts product quality letters into numbers for ML. |
| `failure_type` | Uses the failure flag columns | Gives a readable label like `Power Failure` or `No Failure`. |

The cleaned file is:

```text
data/cleaned/machine_data_cleaned.csv
```

In this repository, the raw file has 10,000 rows and the included cleaned file has 9,894 rows.

## Database And Star Schema

The database part uses PostgreSQL.

The project uses a data warehouse design called a star schema.

### Plain explanation of a star schema

A star schema has one main table in the middle and several smaller lookup tables around it.

The main table is called a fact table. It stores events or measurements.

The smaller tables are called dimension tables. They store descriptions that make the facts easier to group and analyze.

In this project:

- the fact table stores machine operations
- the dimensions store date, product, failure type, and machine condition information

```text
                         dim_date
                            |
dim_product -- fact_machine_operations -- dim_failure_type
                            |
                 dim_machine_condition
```

### Tables

| Table | Type | Purpose |
| --- | --- | --- |
| `staging.machine_data` | Staging table | Temporary clean copy of the machine data before loading into the warehouse. |
| `dw.fact_machine_operations` | Fact table | One row per machine operation. Stores measurements and failure flags. |
| `dw.dim_date` | Dimension table | Calendar information for month, quarter, week, day, and weekend status. |
| `dw.dim_product` | Dimension table | Product ID and product quality category. |
| `dw.dim_failure_type` | Dimension table | Failure codes, names, categories, and severity. |
| `dw.dim_machine_condition` | Dimension table | Tool wear condition, risk level, and recommended action. |

### Why there are simulated dates

The original AI4I dataset does not contain real operation dates.

To support monthly trend analysis, the ETL assigns each row to a random business day in 2023. The random seed is fixed with `random.seed(42)`, which means the result is repeatable.

## OLAP Analysis Files

OLAP means Online Analytical Processing. In plain English, it means summary queries that help people analyze data from different angles.

The dashboard uses four OLAP CSV files.

| CSV file | What it shows |
| --- | --- |
| `dw/OLAP Failure Distribution by Failure Type.csv` | How many records belong to each failure type. |
| `dw/OLAP Failure Rate by Product Quality Type.csv` | Failure rate for low, medium, and high quality products. |
| `dw/OLAP Machine Condition vs Failure Rate.csv` | Failure rate by tool wear condition and risk level. |
| `dw/OLAP Monthly Failure Trend.csv` | Operations and failures by month. |

Current dashboard summary values from the included OLAP CSV files:

| Metric | Value |
| --- | ---: |
| Total operations in dashboard CSVs | 6,390 |
| Total failures | 240 |
| Average failure rate | 3.76% |
| Most common actual failure type | Heat Dissipation Failure |

Failure distribution:

| Failure Type | Occurrences | Percent of All Records |
| --- | ---: | ---: |
| No Failure | 6,145 | 96.17% |
| Heat Dissipation Failure | 80 | 1.25% |
| Power Failure | 65 | 1.02% |
| Overstrain Failure | 55 | 0.86% |
| Tool Wear Failure | 34 | 0.53% |
| Random Failure | 11 | 0.17% |

Machine condition risk:

| Condition | Risk Level | Operations | Failures | Failure Rate |
| --- | --- | ---: | ---: | ---: |
| New Tool (0-100 min) | Low | 2,956 | 76 | 2.57% |
| Mid-Life Tool (100-200 min) | Medium | 2,930 | 84 | 2.87% |
| Aging Tool (200-240 min) | High | 494 | 76 | 15.38% |
| Worn Tool (>240 min) | Critical | 10 | 4 | 40.00% |

## Dashboard Explanation

The dashboard is created in:

```text
app.py
```

It uses Streamlit, which turns Python code into a web app.

The dashboard does not connect directly to PostgreSQL. Instead, it reads the four OLAP CSV files from the `dw` folder.

That means the dashboard can run even if PostgreSQL is not installed, as long as the CSV files are present.

### Dashboard sections

The dashboard contains:

- sidebar filters
- title/header
- KPI cards
- failure distribution bar chart
- monthly failure trend line chart
- machine condition scatter chart
- product quality failure rate bar chart
- detail data tables

### Dashboard filters

The sidebar lets the user filter:

- failure types
- months
- machine conditions

These filters affect the charts shown in the dashboard.

### KPI cards

The top cards show:

- total records
- total failures
- average failure rate
- top failure type

### Charts

| Chart | Purpose |
| --- | --- |
| Failure Distribution by Type | Shows which failures happen most often. |
| Monthly Failure Trend | Shows how failures change month by month. |
| Machine Condition vs Failure Rate | Shows how tool wear condition relates to risk. |
| Failure Rate by Product Quality Type | Shows whether low, medium, or high quality products fail more often. |

## Machine Learning Explanation

The machine learning script is:

```text
ml/xgboost_failure_prediction.py
```

The goal is to predict:

```text
machine_failure
```

That means the model tries to answer:

```text
Given the machine measurements, is this operation likely to fail?
```

### Input features

The model uses these columns:

| Feature | Meaning |
| --- | --- |
| `air_temp_k` | Air temperature in Kelvin. |
| `process_temp_k` | Process temperature in Kelvin. |
| `rotational_speed_rpm` | Rotation speed. |
| `torque_nm` | Machine torque. |
| `tool_wear_min` | Tool wear time. |
| `temp_differential_c` | Difference between process and air temperature. |
| `power_w` | Calculated mechanical power. |
| `type_encoded` | Product quality encoded as a number. |

### Target column

The target is:

```text
machine_failure
```

Values:

- `0` means no failure
- `1` means failure

### Why SMOTE is used

Most machine operations do not fail. This creates an imbalanced dataset.

If the model mostly sees non-failure examples, it may become lazy and predict "no failure" too often.

SMOTE creates synthetic examples of the minority class, which is the failure class. This helps the model learn failure patterns better.

### Why StandardScaler is used

Different columns have different ranges.

For example:

- temperature may be around 300
- torque may be around 40
- power may be thousands

`StandardScaler` puts numeric features on a more comparable scale.

### Why XGBoost is used

XGBoost is a strong machine learning algorithm for tabular data. Tabular data means rows and columns, like a spreadsheet.

It works by building many small decision trees and combining them into a stronger model.

### Outputs

The script saves:

| Output | Purpose |
| --- | --- |
| `ml/xgboost_model.pkl` | Trained model file. |
| `ml/scaler.pkl` | Saved scaler used to transform future input data. |
| `ml/plots/model_evaluation.png` | Confusion matrix, ROC curve, and feature importance. |
| `ml/plots/shap_summary.png` | SHAP explanation plot showing which features influenced predictions. |

## Every Python File Explained

This section explains every project Python file, including the libraries it imports and the main code sections or functions.

### Python terms used below

| Term | Simple meaning |
| --- | --- |
| Python file | A file ending in `.py`. It contains Python instructions. |
| Library | Extra code someone else wrote so you do not have to build everything yourself. |
| Import | A line that loads a library into the file. Example: `import pandas as pd`. |
| Function | A named block of code that performs a specific job. |
| DataFrame | A table in Python, like an Excel sheet. pandas uses DataFrames. |
| Script | A Python file meant to be run from start to finish. |
| Module | A Python file or imported package. In this README, "module" can also refer to a major code section inside a script. |

### `app.py`

Purpose: creates the Streamlit web dashboard.

Run it with:

```powershell
streamlit run app.py
```

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `import streamlit as st` | Creates the web dashboard: page layout, sidebar, metrics, tabs, and charts. |
| `import pandas as pd` | Reads CSV files into DataFrames and filters data. |
| `import plotly.express as px` | Quickly creates Plotly bar and scatter charts. |
| `import plotly.graph_objects as go` | Creates a more customized line chart for monthly trend. |

Main function:

| Function | Purpose |
| --- | --- |
| `load_data()` | Reads the four OLAP CSV files from `dw/`, cleans extra spaces from month names, and returns four DataFrames. It is decorated with `@st.cache_data`, so Streamlit does not reread the files every time the page refreshes. |

Main code sections:

| Section | What it does |
| --- | --- |
| Page config | Sets dashboard title, icon, and wide layout. |
| Data loading | Calls `load_data()` and stores the four OLAP DataFrames. |
| Sidebar filters | Creates multi-select filters for failure type, month, and machine condition. |
| Filter application | Uses pandas `.isin()` to keep only selected rows. |
| Header | Displays the dashboard title and subtitle. |
| KPI cards | Calculates total records, total failures, average failure rate, and top failure type. |
| Row 1 charts | Builds failure distribution and monthly trend charts. |
| Row 2 charts | Builds machine condition and product quality charts. |
| Data tables | Shows the raw OLAP tables in Streamlit tabs. |

Important data files used:

```text
dw/OLAP Failure Distribution by Failure Type.csv
dw/OLAP Failure Rate by Product Quality Type.csv
dw/OLAP Machine Condition vs Failure Rate.csv
dw/OLAP Monthly Failure Trend.csv
```

### `run_etl.py`

Purpose: main end-to-end ETL pipeline.

Run it with:

```powershell
python run_etl.py
```

Before running, set:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/co4031_dw"
```

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `os` | Reads environment variables, especially `DATABASE_URL`. |
| `sys` | Stops the script with `sys.exit(1)` if `DATABASE_URL` is missing. |
| `warnings` | Hides warning messages to keep terminal output cleaner. |
| `pandas as pd` | Reads CSV files, cleans data, creates DataFrames, writes SQL tables. |
| `numpy as np` | Calculates pi and mechanical power. |
| `sqlalchemy.create_engine` | Creates a connection engine for PostgreSQL. |
| `sqlalchemy.text` | Safely wraps raw SQL statements before executing them. |
| `datetime.date` | Represents dates for simulated operation dates. |
| `datetime.timedelta` | Supports date arithmetic, although this script mostly uses dates from `dim_date`. |
| `random` | Randomly assigns each operation to a business day. |
| `matplotlib` | Sets non-interactive plotting backend. |
| `matplotlib.pyplot as plt` | Imported for plotting support, though this script mainly focuses on ETL output. |
| `seaborn as sns` | Imported for visualization support. |

Functions:

| Function | Purpose |
| --- | --- |
| `remove_iqr_outliers(df, col, factor=3.0)` | Removes extreme outlier rows for one numeric column using the IQR method. |
| `get_failure_type(row)` | Reads the failure flag columns and returns a readable failure label. |
| `get_failure_code(row)` | Converts failure flags into warehouse failure codes such as `TWF`, `HDF`, `PWF`, `OSF`, `RNF`, or `NF`. |
| `get_condition_code(wear_min)` | Converts tool wear minutes into condition codes such as `NEW_TOOL`, `MID_TOOL`, `OLD_TOOL`, or `WORN_TOOL`. |

Main code sections:

| Section | What it does |
| --- | --- |
| Database connection | Reads `DATABASE_URL`, creates a SQLAlchemy engine, and stops if the variable is missing. |
| Step 1: Loading and cleaning | Reads raw CSV, checks data quality, removes duplicates, fills missing values, removes impossible records and outliers. |
| Step 2: Feature engineering | Creates Celsius temperatures, temperature differential, power, numeric quality type, and readable failure type. |
| Step 3: Load to staging | Creates `staging.machine_data` and loads the cleaned DataFrame into PostgreSQL. |
| Step 4: Populate star schema | Fills product dimension and fact table, maps failure types, maps machine condition, assigns dates, and inserts fact rows. |
| Step 5: OLAP analysis | Runs summary SQL queries and prints results to the terminal. |

Important inputs:

```text
data/raw/ai4i2020.csv
dw/01_create_star_schema.sql must already have been run
DATABASE_URL environment variable
```

Important outputs:

```text
data/cleaned/machine_data_cleaned.csv
staging.machine_data
dw.dim_product
dw.fact_machine_operations
printed OLAP summaries
```

Important limitation:

`run_etl.py` prints OLAP summaries but does not export the four dashboard CSV files automatically. To fully refresh the dashboard files, run the OLAP SQL files and export their results as CSV.

### `main.py`

Purpose: placeholder Python entry file.

Libraries imported:

```text
None
```

Function:

| Function | Purpose |
| --- | --- |
| `main()` | Prints `Hello from repl-nix-workspace!`. It is not part of the real dashboard, ETL, database, or ML workflow. |

Main code:

```python
if __name__ == "__main__":
    main()
```

This means: if someone runs `python main.py`, Python calls `main()`.

### `data/raw/01_exploration.py`

Purpose: older step-by-step exploration and preprocessing script.

Run it with:

```powershell
python data\raw\01_exploration.py
```

Important path note: this file currently uses hard-coded paths like:

```text
C:\co4031_project\data\raw\ai4i2020.csv
```

If your project is not located at `C:\co4031_project`, update the path variables before running this file. For normal use, `run_etl.py` is more portable.

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `pandas as pd` | Reads the raw CSV, cleans tables, calculates correlations, saves cleaned CSV. |
| `numpy as np` | Calculates mechanical power using pi. |
| `matplotlib.pyplot as plt` | Creates and saves distribution plots and heatmaps. |
| `seaborn as sns` | Creates the correlation heatmap. |
| `os` | Creates the cleaned data folder if needed. |
| `warnings` | Hides warnings for cleaner output. |

Functions:

| Function | Purpose |
| --- | --- |
| `remove_iqr_outliers(df, col, factor=3.0)` | Removes extreme outliers from selected numeric columns. |
| `get_failure_type(row)` | Creates a readable failure label from the binary failure columns. |

Main code sections:

| Section | What it does |
| --- | --- |
| Paths | Defines raw CSV path, cleaned CSV path, and plot output paths. |
| Section 1: Load raw data | Reads the original CSV and prints shape, first rows, and data types. |
| Section 2: Data quality inspection | Prints missing values, duplicate count, and descriptive statistics. |
| Section 3: Data cleaning | Removes duplicates, fills missing values, removes impossible values, and removes outliers. |
| Section 4: Transformation | Converts temperatures, creates power and failure labels, and renames columns. |
| Section 5: Correlation analysis | Shows how numeric features correlate with machine failure. |
| Section 6: Save cleaned dataset | Writes `machine_data_cleaned.csv`. |
| Section 7: Visualisations | Saves feature distribution plots and a correlation heatmap. |

Outputs:

```text
data/cleaned/machine_data_cleaned.csv
data/cleaned/eda_distributions.png
data/cleaned/correlation_heatmap.png
```

### `etl/02 _load_to_dw.py`

Purpose: older script that loads the cleaned CSV into the PostgreSQL staging table.

Run it with:

```powershell
python "etl\02 _load_to_dw.py"
```

Important path and credential note: this file contains hard-coded database settings:

```python
DB_USER = "postgres"
DB_PASSWORD = "885028"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "co4031_dw"
```

It also uses this hard-coded cleaned file path:

```text
C:\co4031_project\data\cleaned\machine_data_cleaned.csv
```

Change those values before running on another computer. For normal use, prefer `run_etl.py`, which uses `DATABASE_URL`.

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `pandas as pd` | Reads the cleaned CSV and writes it to PostgreSQL. |
| `sqlalchemy.create_engine` | Creates the PostgreSQL connection engine. |
| `sqlalchemy.text` | Runs SQL commands such as `SELECT version()` and `SELECT COUNT(*)`. |
| `warnings` | Hides warning messages. |

Functions:

```text
No custom functions are defined in this file.
```

Main code sections:

| Section | What it does |
| --- | --- |
| Connection configuration | Stores PostgreSQL username, password, host, port, and database name. |
| Build connection string | Creates a PostgreSQL URL from those settings. |
| Test connection | Connects to PostgreSQL and prints the server version. |
| Load cleaned CSV | Reads `machine_data_cleaned.csv` into a pandas DataFrame. |
| Rename columns | Converts some derived column names to lowercase database-friendly names. |
| Load staging table | Uses `df.to_sql()` to write data to `staging.machine_data`. |
| Verify load | Counts rows in the staging table and prints sample rows. |

Important caution:

The script defines a `db_columns` list but does not use it to select columns. The actual load uses the full DataFrame after renaming columns.

### `dw/02_populate_star.py`

Purpose: older script that reads `staging.machine_data` and populates the star schema.

Run it with:

```powershell
python dw\02_populate_star.py
```

Important credential note: this file also contains hard-coded database settings. Change `DB_PASSWORD` and related settings before running on another machine.

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `pandas as pd` | Reads database tables into DataFrames and writes dimension/fact tables. |
| `sqlalchemy.create_engine` | Creates the PostgreSQL connection engine. |
| `sqlalchemy.text` | Runs SQL delete and verification commands. |
| `numpy as np` | Imported, but not meaningfully used in the current script. |
| `datetime.date` | Creates simulated start date. |
| `datetime.timedelta` | Moves one day at a time when building simulated business days. |
| `random` | Assigns each machine row to a simulated business day. |
| `warnings` | Hides warning messages. |

Functions:

| Function | Purpose |
| --- | --- |
| `get_failure_code(row)` | Converts binary failure flags into a single failure code used by `dw.dim_failure_type`. |
| `get_condition_code(wear_min)` | Converts tool wear minutes into a machine condition code used by `dw.dim_machine_condition`. |

Main code sections:

| Section | What it does |
| --- | --- |
| Connection configuration | Defines PostgreSQL connection details and creates the engine. |
| Load staging data | Reads `staging.machine_data`. |
| Populate `dim_product` | Creates product dimension rows from unique product IDs and quality types. |
| Map failure type | Looks up failure type keys and assigns `failure_type_fk`. |
| Map machine condition | Converts tool wear into condition code and assigns `condition_fk`. |
| Simulate dates | Creates business days and assigns each operation a simulated date. |
| Populate fact table | Creates `fact_machine_operations` rows with foreign keys and measurements. |
| Verify | Prints total inserted fact rows and failure rows. |

Inputs:

```text
staging.machine_data
dw.dim_date
dw.dim_failure_type
dw.dim_machine_condition
```

Outputs:

```text
dw.dim_product
dw.fact_machine_operations
```

### `ml/xgboost_failure_prediction.py`

Purpose: trains a machine learning model to predict machine failure.

Run it with:

```powershell
python ml\xgboost_failure_prediction.py
```

Libraries imported:

| Import | What it does in this file |
| --- | --- |
| `pandas as pd` | Reads cleaned CSV and handles feature/target tables. |
| `numpy as np` | Sets random seed and sorts feature importance values. |
| `matplotlib.pyplot as plt` | Creates and saves evaluation plots. |
| `seaborn as sns` | Imported for visualization support, though not heavily used in this script. |
| `sklearn.model_selection.train_test_split` | Splits data into training and test sets. |
| `sklearn.model_selection.cross_val_score` | Runs 5-fold cross-validation. |
| `sklearn.preprocessing.StandardScaler` | Scales numeric features. |
| `sklearn.metrics.classification_report` | Prints precision, recall, f1-score, and support. |
| `sklearn.metrics.confusion_matrix` | Builds confusion matrix values. |
| `sklearn.metrics.roc_auc_score` | Measures how well the model separates failure from non-failure. |
| `sklearn.metrics.roc_curve` | Creates values for the ROC curve. |
| `sklearn.metrics.precision_recall_curve` | Imported, but not used in the current plotting code. |
| `sklearn.metrics.ConfusionMatrixDisplay` | Draws the confusion matrix. |
| `imblearn.over_sampling.SMOTE` | Balances the training data by creating synthetic failure examples. |
| `xgboost as xgb` | Provides the XGBoost classifier. |
| `shap` | Creates model explanation values and summary plot. |
| `pickle` | Saves the trained model and scaler to `.pkl` files. |
| `os` | Builds paths and creates the plots directory. |
| `warnings` | Hides warning messages. |

Functions:

```text
No custom functions are defined in this file.
```

Main code sections:

| Section | What it does |
| --- | --- |
| Configuration | Defines paths, plot folder, and random seed. |
| Step 1: Load data | Reads `data/cleaned/machine_data_cleaned.csv`. |
| Feature selection | Chooses model input columns and target column. |
| Column fallback | Handles lowercase column names by copying them to expected names if needed. |
| Step 2: SMOTE | Splits train/test data and balances the training set. |
| Step 3: Feature scaling | Fits `StandardScaler` and saves it to `ml/scaler.pkl`. |
| Step 4: Train XGBoost | Trains `XGBClassifier` with fixed hyperparameters. |
| Step 5: Evaluate model | Prints classification report and ROC-AUC. |
| Step 6: Plot results | Saves confusion matrix, ROC curve, and feature importance. |
| Step 7: SHAP analysis | Saves a plot explaining which features most affect model predictions. |
| Step 8: Cross-validation | Runs 5-fold ROC-AUC cross-validation. |

Important output files:

```text
ml/xgboost_model.pkl
ml/scaler.pkl
ml/plots/model_evaluation.png
ml/plots/shap_summary.png
```

## Every Important Non-Python File Explained

### `pyproject.toml`

This file defines the Python project name, version, required Python version, and dependencies.

It says:

```text
requires-python = ">=3.11"
```

So Python 3.11 or newer should be used.

### `.streamlit/config.toml`

This file controls Streamlit server settings:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

Simple meaning:

- `headless = true`: Streamlit can run without opening a browser automatically.
- `address = "0.0.0.0"`: the app listens on all network interfaces.
- `port = 5000`: the app tries to use port 5000.

### `etl/staging.sql`

Creates the staging schema and table:

```text
staging.machine_data
```

The staging table stores cleaned machine data before it is transformed into the warehouse fact and dimension tables.

### `dw/01_create_star_schema.sql`

Creates the data warehouse schema:

```text
dw
```

Creates and fills:

- `dw.dim_date`
- `dw.dim_failure_type`
- `dw.dim_machine_condition`

Creates empty:

- `dw.dim_product`
- `dw.fact_machine_operations`

Those two are filled later from the cleaned machine data.

### `dw/OLAP *.sql`

These files contain analytical SQL queries:

| SQL file | Purpose |
| --- | --- |
| `OLAP Failure Distribution by Failure Type.sql` | Counts records by failure type. |
| `OLAP Failure Rate by Product Quality Type.sql` | Calculates failure rate by product quality. |
| `OLAP Machine Condition vs Failure Rate.sql` | Calculates failure rate by machine condition. |
| `OLAP Monthly Failure Trend.sql` | Calculates monthly operations and failures. |

### `dw/OLAP *.csv`

These files are exported results from the OLAP SQL files.

The dashboard reads these CSV files directly.

### `etl/machine_etl.ktr`

This is a Pentaho/Kettle transformation file. It represents an ETL workflow in a visual ETL tool. The Python workflow can be used without opening this file.

### `picture/`

Contains dashboard screenshots.

These are useful for reports and presentations.

### `report/`

Contains report assets, diagrams, screenshots, and LaTeX report files.

## Common Problems And Fixes

### Problem: `streamlit` is not recognized

Cause: dependencies are not installed or the virtual environment is not active.

Fix:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e .
streamlit run app.py
```

### Problem: dashboard cannot find a CSV file

Cause: `app.py` expects OLAP CSV files in `dw/`.

Fix: make sure these files exist:

```text
dw/OLAP Failure Distribution by Failure Type.csv
dw/OLAP Failure Rate by Product Quality Type.csv
dw/OLAP Machine Condition vs Failure Rate.csv
dw/OLAP Monthly Failure Trend.csv
```

### Problem: `DATABASE_URL environment variable not set`

Cause: `run_etl.py` requires `DATABASE_URL`.

Fix in PowerShell:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/co4031_dw"
python run_etl.py
```

### Problem: PostgreSQL authentication failed

Cause: wrong username, password, host, port, or database name.

Fix: check your PostgreSQL login details and update the connection string.

### Problem: relation `dw.fact_machine_operations` does not exist

Cause: the star schema SQL was not run before the ETL.

Fix:

```powershell
psql -U postgres -d co4031_dw -f "dw\01_create_star_schema.sql"
python run_etl.py
```

### Problem: ML script says a package is missing

Cause: ML dependencies are not included in the core dependency list.

Fix:

```powershell
pip install scikit-learn imbalanced-learn xgboost shap
```

### Problem: old scripts cannot find `C:\co4031_project`

Cause: some earlier step scripts use hard-coded paths.

Fix: either edit the path variables in those files or use `run_etl.py`, which uses project-relative paths for input and output files.

## Recommended Presentation Flow

For a project defense or walkthrough, use this order:

1. Explain the manufacturing failure problem.
2. Show the raw AI4I dataset columns.
3. Explain data cleaning and feature engineering.
4. Show the cleaned dataset.
5. Explain staging vs data warehouse.
6. Show the star schema: fact table in the center, dimensions around it.
7. Explain each OLAP query.
8. Open the Streamlit dashboard and demonstrate filters.
9. Explain the ML model as an optional predictive extension.
10. Show model evaluation and SHAP plot.

## Short Version

If you only remember one thing:

```text
app.py reads OLAP CSV files and shows the dashboard.
run_etl.py rebuilds the cleaned data and PostgreSQL warehouse.
ml/xgboost_failure_prediction.py trains the optional failure prediction model.
```

