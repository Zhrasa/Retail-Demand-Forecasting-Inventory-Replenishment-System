# Retail-Demand-Forecasting-Inventory-Replenishment-System
Simulate a demand forecasting and replenishment system using historical sales data, and build a dashboard to monitor KPIs like stock levels, sell-through rate, and forecast accuracy.

##Core Features:
Data Cleaning & Transformation:

Load historical retail sales data.

Clean and reshape it (daily or weekly granularity by product/store).

Demand Forecasting:

Use time series models (ARIMA, Prophet) or machine learning (XGBoost, LSTM).

Predict demand for the next 30/60 days.

Safety Stock Calculation:

Implement a basic EOQ (Economic Order Quantity) or service level-based safety stock calculation.

Inventory Replenishment Logic:

Trigger replenishment orders based on forecast, current stock, lead time.

Simulate stock movements (purchases, replenishment, stockouts).

Dashboard & Reporting:

Power BI or Streamlit dashboard to visualize:

Forecast vs. actual demand

Inventory turnover ratio

Replenishment recommendations
