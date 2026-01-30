import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

class AnomalyDetector:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.model_path = os.path.join(BASE_DIR, "models", "anomaly_model.joblib")

    def train(self, data_path):
        df = pd.read_csv(data_path)
        
        # Features for anomaly detection
        X = df[['price', 'quantity', 'total_amount']]
        
        # Isolation Forest
        clf = IsolationForest(contamination=0.01, random_state=42)
        clf.fit(X)
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(clf, self.model_path)
        print("Anomaly Detection model trained and saved.")

    def detect(self, data):
        # data should be a dict or dataframe with price, quantity, total_amount
        if not os.path.exists(self.model_path):
            return None
        
        clf = joblib.load(self.model_path)
        df = pd.DataFrame([data])
        X = df[['price', 'quantity', 'total_amount']]
        
        prediction = clf.predict(X) # -1 for anomaly, 1 for normal
        return bool(prediction[0] == -1)
