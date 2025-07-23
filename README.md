# 🛒 Retail Demand Forecasting & Inventory Replenishment Simulator

This project replicates a simplified **RELEX-like inventory optimization system**, built using Python for forecasting, simulation, and dashboarding.

---

## 📌 Core Features

### 📊 1. Data Cleaning & Transformation
- Load historical retail sales data (e.g. from Kaggle or synthetic sources).
- Clean and reshape for analysis — **daily or weekly** granularity by `product-store` pairs.
- Handle missing values, outliers, and seasonality patterns.

---

### 📈 2. Demand Forecasting
- Predict demand for the next **30/60 days** using:
  - **Time series models**: ARIMA, Facebook Prophet.
  - **Machine learning**: XGBoost, LightGBM.
  - *(Optional advanced)*: LSTM (deep learning model).
- Cross-validate with backtesting over historical windows.

---

### 📦 3. Safety Stock Calculation
- Implement simplified inventory policies:
  - **EOQ (Economic Order Quantity)**.
  - **Service-level based** safety stock using standard deviation of demand and desired service level (e.g., 95%).

---

### 🔁 4. Inventory Replenishment Logic
- Trigger **replenishment orders** based on:
  - Forecasted demand.
  - Current stock.
  - Lead time and reorder points.
- Simulate **stock movements**:
  - Purchases.
  - Replenishments.
  - Stockouts.

---

### 📊 5. Dashboard & Reporting (Power BI / Streamlit)
Interactive dashboards showing:

- 📉 Forecast vs. Actual Demand  
- 🔁 Inventory Turnover Ratio  
- 🚨 Stockout Alerts  
- 📦 Replenishment Recommendations  

---

## 🧰 Tech Stack

- **Python** (Pandas, Scikit-learn, Prophet, XGBoost)
- **Streamlit** or **Power BI** for dashboard
- **SQL or SQLite** for local data handling
- **Git + Git LFS** for versioning large CSVs

---


