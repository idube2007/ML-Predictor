import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os

class CustomerSegmenter:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.model_path = os.path.join(BASE_DIR, "models", "segmentation_model.joblib")
        self.scaler_path = os.path.join(BASE_DIR, "models", "segmentation_scaler.joblib")

    def train(self, data_path):
        df = pd.read_csv(data_path)
        
        # Features for segmentation
        X = df[['age', 'annual_income', 'loyalty_score']]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(X_scaled)
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(kmeans, self.model_path)
        joblib.dump(scaler, self.scaler_path)
        print("Customer Segmentation model trained and saved.")

    def get_segments(self, data_path):
        if not os.path.exists(self.model_path):
            return None
        
        df = pd.read_csv(data_path)
        kmeans = joblib.load(self.model_path)
        scaler = joblib.load(self.scaler_path)
        
        X = df[['age', 'annual_income', 'loyalty_score']]
        X_scaled = scaler.transform(X)
        df['segment'] = kmeans.predict(X_scaled)
        
        return df[['customer_id', 'segment']].to_dict(orient='records')
