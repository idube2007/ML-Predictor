import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.le_category = LabelEncoder()
        self.model_path = 'd:/MLAPP/sris/models/price_model.joblib'
        self.le_path = 'd:/MLAPP/sris/models/le_category.joblib'

    def train(self, data_path):
        df = pd.read_csv(data_path)
        # Feature Engineering
        df['category_encoded'] = self.le_category.fit_transform(df['category'])
        
        X = df[['category_encoded']] # Simplified for this demo
        y = df['price']
        
        self.model.fit(X, y)
        
        # Save models
        os.makedirs('d:/MLAPP/sris/models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.le_category, self.le_path)
        print("Price Prediction model trained and saved.")

    def predict(self, category):
        if not os.path.exists(self.model_path):
            return None
        
        model = joblib.load(self.model_path)
        le = joblib.load(self.le_path)
        
        cat_encoded = le.transform([category])[0]
        prediction = model.predict([[cat_encoded]])
        return round(float(prediction[0]), 2)
