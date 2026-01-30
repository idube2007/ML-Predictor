import pandas as pd
import numpy as np
import joblib
import os

class DemandForecaster:
    def __init__(self):
        self.model_path = 'd:/MLAPP/sris/models/demand_model.joblib'

    def train(self, data_path):
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by date and category to get daily demand
        daily_demand = df.groupby(['date', 'category'])['quantity'].sum().reset_index()
        
        # In a real scenario, we'd use Prophet or ARIMA here. 
        # For this demo, we'll store historical averages as a simple predictor.
        history = daily_demand.groupby('category')['quantity'].mean().to_dict()
        
        os.makedirs('d:/MLAPP/sris/models', exist_ok=True)
        joblib.dump(history, self.model_path)
        print("Demand Forecasting model (Historical Avg) trained and saved.")

    def predict(self, category):
        if not os.path.exists(self.model_path):
            return None
        
        history = joblib.load(self.model_path)
        avg_demand = history.get(category, 0)
        
        # Return a simple 7-day forecast with some noise
        forecast = [round(avg_demand * np.random.uniform(0.8, 1.2), 2) for _ in range(7)]
        return forecast
