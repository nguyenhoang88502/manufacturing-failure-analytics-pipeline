# 🏭 Manufacturing Failure Analysis Dashboard

> **CO4031 BTL — Data Warehouse & Business Intelligence System**  
> Phân tích dữ liệu lỗi máy sản xuất bằng ETL Pipeline, Star Schema và Streamlit Dashboard.

---

## 📁 Cấu trúc thư mục

```
├── app.py                          # Streamlit dashboard (chạy file này)
├── run_etl.py                      # ETL pipeline: làm sạch → staging → star schema → OLAP
│
├── data/
│   ├── raw/
│   │   ├── ai4i2020.csv            # Dataset gốc (AI4I 2020 Predictive Maintenance)
│   │   └── 01_exploration.py       # Script khám phá dữ liệu thô
│   └── cleaned/
│       ├── machine_data_cleaned.csv    # Dữ liệu sau khi làm sạch (tự sinh khi chạy ETL)
│       ├── eda_distributions.png       # Biểu đồ phân phối đặc trưng
│       └── correlation_heatmap.png     # Heatmap tương quan
│
├── etl/
│   ├── staging.sql                 # DDL tạo bảng staging
│   ├── 02 _load_to_dw.py          # Script nạp dữ liệu vào staging (phiên bản gốc)
│   └── machine_etl.ktr             # Kettle/PDI ETL transformation file
│
├── dw/
│   ├── 01_create_star_schema.sql   # DDL tạo toàn bộ Star Schema
│   ├── 02_populate_star.py         # Script nạp dữ liệu vào DW (phiên bản gốc)
│   ├── OLAP Failure Distribution by Failure Type.csv   # Kết quả OLAP
│   ├── OLAP Failure Rate by Product Quality Type.csv   # Kết quả OLAP
│   ├── OLAP Machine Condition vs Failure Rate.csv      # Kết quả OLAP
│   ├── OLAP Monthly Failure Trend.csv                  # Kết quả OLAP
│   └── *.sql                       # Các câu truy vấn OLAP
│
├── picture/                        # Ảnh chụp toàn bộ chức năng dashboard
├── pyproject.toml                  # Danh sách dependencies Python
└── .streamlit/config.toml          # Cấu hình Streamlit server
```

---

## 🗄️ Kiến trúc Data Warehouse (Star Schema)

```
                    ┌──────────────┐
                    │  dim_date    │
                    └──────┬───────┘
                           │
┌──────────────┐    ┌──────┴───────────────────┐    ┌───────────────────────┐ 
│  dim_product │────│  fact_machine_operations │────│   dim_failure_type    │
└──────────────┘    └──────┬───────────────────┘    └───────────────────────┘
                           │
                    ┌──────┴──────────────────┐
                    │  dim_machine_condition  │
                    └─────────────────────────┘
```

**Fact table:** `fact_machine_operations` (~9,894 bản ghi)  
**Dimensions:** `dim_date`, `dim_product`, `dim_failure_type`, `dim_machine_condition`

---

## 🚀 Hướng dẫn chạy trên máy cá nhân (Local)

### 1. Clone repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Cài đặt Python dependencies

```bash
pip install streamlit plotly pandas sqlalchemy psycopg2-binary numpy matplotlib seaborn
```

Hoặc dùng `pyproject.toml`:

```bash
pip install .
```

### 3. Xem Dashboard ngay (không cần Database)

Dashboard đọc trực tiếp từ file CSV trong thư mục `dw/` — **không cần cài PostgreSQL**:

```bash
streamlit run app.py
```

Mở trình duyệt tại: **http://localhost:8501**

---

### 4. (Tùy chọn) Chạy toàn bộ ETL Pipeline

Nếu muốn chạy lại pipeline đầy đủ từ dữ liệu thô → Star Schema:

**Bước 4a:** Cài PostgreSQL và tạo database, sau đó đặt biến môi trường:

```bash
# Linux / macOS
export DATABASE_URL="postgresql://username:password@localhost:5432/your_database"

# Windows PowerShell
$env:DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

# Windows CMD
set DATABASE_URL=postgresql://username:password@localhost:5432/your_database
```

**Bước 4b:** Chạy ETL pipeline:

```bash
python run_etl.py
```

Pipeline sẽ thực hiện lần lượt:
1. Tải và làm sạch dữ liệu thô (`data/raw/ai4i2020.csv`)
2. Feature engineering (K→°C, tính Power, mã hóa nhãn lỗi)
3. Nạp vào bảng staging (`staging.machine_data`)
4. Populate Star Schema (`dw.*`)
5. Chạy OLAP queries và in kết quả ra console

---

## 📊 Các chức năng Dashboard

| Chức năng | Mô tả |
|-----------|-------|
| **KPI Cards** | Tổng records, tổng lỗi, tỷ lệ lỗi trung bình, loại lỗi phổ biến nhất |
| **Failure Distribution** | Biểu đồ cột phân bố các loại lỗi (trừ "No Failure") |
| **Monthly Trend** | Biểu đồ đường xu hướng lỗi theo từng tháng năm 2023 |
| **Machine Condition** | Scatter plot: điều kiện máy vs tỷ lệ lỗi (bubble size = số lỗi) |
| **Product Quality** | Biểu đồ cột tỷ lệ lỗi theo phân loại chất lượng sản phẩm |
| **Data Tables** | Bảng dữ liệu đầy đủ theo tab cho cả 4 OLAP datasets |
| **Sidebar Filters** | Lọc theo Failure Type, Month, Machine Condition — tất cả charts cập nhật real-time |

---

## 📦 Dataset

**AI4I 2020 Predictive Maintenance Dataset**

- Nguồn: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset)
- 10,000 bản ghi, 14 đặc trưng
- Các đặc trưng chính: Air Temperature, Process Temperature, Rotational Speed, Torque, Tool Wear
- Nhãn: Machine Failure + 5 loại lỗi (TWF, HDF, PWF, OSF, RNF)

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Dashboard | Streamlit + Plotly |
| ETL & Data Processing | Python, Pandas, NumPy |
| Database | PostgreSQL |
| ORM / Connector | SQLAlchemy, psycopg2 |
| Visualization | Plotly Express, Matplotlib, Seaborn |
| DW Schema | Star Schema (Fact + 4 Dimensions) |
