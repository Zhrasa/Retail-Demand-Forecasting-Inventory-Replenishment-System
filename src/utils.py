import pandas as pd
import numpy as np
from typing import Dict, List

def load_data(file_path: str) -> pd.DataFrame:
    """Load and validate input data"""
    data = pd.read_csv(file_path)
    required_columns = ['Date', 'Store', 'Product', 'Sales']
    
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")
    
    return data

def calculate_kpis(inventory_data: pd.DataFrame) -> Dict:
    """Calculate inventory KPIs"""
    avg_stock = inventory_data['stock_level'].mean()
    total_sales = inventory_data['sales'].sum()
    stockouts = (inventory_data['stock_level'] <= 0).sum()
    days_of_coverage = avg_stock / (total_sales / len(inventory_data)) if total_sales > 0 else np.inf
    
    return {
        'average_stock': avg_stock,
        'total_sales': total_sales,
        'stockout_days': stockouts,
        'days_of_coverage': days_of_coverage,
        'stockout_rate': stockouts / len(inventory_data)
    }

def prepare_forecast_data(forecast: pd.DataFrame, actual: pd.DataFrame) -> pd.DataFrame:
    """Combine forecast and actual data for visualization"""
    merged = pd.merge(
        forecast.rename(columns={'yhat': 'forecast'}),
        actual.rename(columns={'Sales': 'actual'}),
        on='Date',
        how='left'
    )
    merged['error'] = merged['actual'] - merged['forecast']
    merged['ape'] = (np.abs(merged['error']) / merged['actual']) * 100
    return merged
