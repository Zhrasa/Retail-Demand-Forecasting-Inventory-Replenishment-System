import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.forecasting import DemandForecaster
from src.replenishment import InventoryManager
from src.utils import load_data, calculate_kpis, prepare_forecast_data

# Page configuration
st.set_page_config(page_title="Retail Demand Forecasting", layout="wide")

# Sidebar for inputs
st.sidebar.header("Configuration")
data_file = st.sidebar.file_uploader("Upload sales data", type=['csv'])
forecast_method = st.sidebar.selectbox("Forecasting method", ['prophet', 'arima'])
forecast_periods = st.sidebar.slider("Forecast periods (days)", 7, 90, 30)

# Main content
st.title("Retail Demand Forecasting & Inventory Replenishment")

if data_file is not None:
    # Load and process data
    data = load_data(data_file)
    forecaster = DemandForecaster(data)
    daily_sales = forecaster.preprocess_data()
    
    # Generate forecast
    forecast = forecaster.forecast_demand(method=forecast_method, periods=forecast_periods)
    
    # Display forecast
    st.subheader("Demand Forecast")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=daily_sales, x='Date', y='Sales', label='Historical', ax=ax)
    sns.lineplot(data=forecast, x='Date', y='yhat', label='Forecast', ax=ax)
    if 'yhat_lower' in forecast.columns:
        ax.fill_between(forecast['Date'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    st.pyplot(fig)
    
    # Inventory management
    st.subheader("Inventory Replenishment")
    
    # Simplified inventory simulation
    current_inventory = {'Product1': 100, 'Product2': 150}  # Example data
    demand_std = daily_sales['Sales'].std()
    demand_mean = daily_sales['Sales'].mean()
    
    inventory_mgr = InventoryManager(
        demand_forecast=forecast,
        current_inventory=current_inventory,
        lead_time=7,
        service_level=0.95
    )
    
    # Generate recommendations for each product
    recommendations = []
    for product in current_inventory.keys():
        rec = inventory_mgr.generate_replenishment_orders(
            product_id=product,
            daily_demand_mean=demand_mean,
            daily_demand_std=demand_std
        )
        recommendations.append(rec)
    
    st.dataframe(pd.DataFrame(recommendations))
    
    # KPIs
    st.subheader("Key Performance Indicators")
    simulated_inventory = inventory_mgr.simulate_stock_movement(
        product_id='Product1',
        orders=[],
        sales_data=daily_sales.tail(30)
    )
    kpis = calculate_kpis(simulated_inventory)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Stock", f"{kpis['average_stock']:.0f}")
    col2.metric("Stockout Days", kpis['stockout_days'])
    col3.metric("Days of Coverage", f"{kpis['days_of_coverage']:.1f}")
    col4.metric("Stockout Rate", f"{kpis['stockout_rate']*100:.1f}%")
    
    # Forecast accuracy
    if len(daily_sales) > forecast_periods:
        actual = daily_sales.tail(forecast_periods)
        forecast_accuracy = prepare_forecast_data(forecast.head(forecast_periods), actual)
        mape = forecast_accuracy['ape'].mean()
        
        st.subheader("Forecast Accuracy")
        st.metric("Mean Absolute Percentage Error", f"{mape:.1f}%")
        
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=forecast_accuracy, x='Date', y='actual', label='Actual', ax=ax2)
        sns.lineplot(data=forecast_accuracy, x='Date', y='forecast', label='Forecast', ax=ax2)
        ax2.fill_between(forecast_accuracy['Date'], 
                        forecast_accuracy['forecast'] - forecast_accuracy['error'],
                        forecast_accuracy['forecast'] + forecast_accuracy['error'],
                        alpha=0.2)
        st.pyplot(fig2)
else:
    st.info("Please upload a sales data file to get started")
