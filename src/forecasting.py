import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from fbprophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from typing import Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

class DemandForecaster:
    def __init__(self, data: pd.DataFrame):
        """Initialize with historical sales data"""
        self.data = data
        self.preprocessed = False
        
    def preprocess_data(self) -> pd.DataFrame:
        """Clean and prepare the data for forecasting"""
        # Convert date column to datetime
        if 'Date' in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self.data = self.data.sort_values('Date')
        
        # Handle missing values
        self.data = self.data.fillna(method='ffill').fillna(0)
        
        # Aggregate to daily level if needed
        if 'Sales' in self.data.columns:
            self.daily_sales = self.data.groupby('Date')['Sales'].sum().reset_index()
        
        self.preprocessed = True
        return self.daily_sales
    
    def train_arima(self, train_data: pd.Series, order: Tuple = (5,1,0)) -> Tuple[any, pd.Series]:
        """Train ARIMA model"""
        model = ARIMA(train_data, order=order)
        model_fit = model.fit()
        return model_fit
    
    def train_prophet(self, train_data: pd.DataFrame) -> any:
        """Train Facebook Prophet model"""
        prophet_data = train_data.rename(columns={'Date': 'ds', 'Sales': 'y'})
        model = Prophet()
        model.fit(prophet_data)
        return model
    
    def evaluate_model(self, actual: pd.Series, predicted: pd.Series) -> Dict:
        """Calculate evaluation metrics"""
        mae = mean_absolute_error(actual, predicted)
        mse = mean_squared_error(actual, predicted)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        
        return {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'MAPE': mape
        }
    
    def forecast_demand(self, method: str = 'prophet', periods: int = 30) -> pd.DataFrame:
        """Generate demand forecasts"""
        if not self.preprocessed:
            self.preprocess_data()
            
        if method == 'prophet':
            model = self.train_prophet(self.daily_sales)
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(columns={'ds': 'Date'})
        
        elif method == 'arima':
            model = self.train_arima(self.daily_sales['Sales'])
            forecast = model.forecast(steps=periods)
            dates = pd.date_range(start=self.daily_sales['Date'].max(), periods=periods+1, closed='right')
            return pd.DataFrame({'Date': dates, 'yhat': forecast})
        
        else:
            raise ValueError("Unsupported forecasting method")
