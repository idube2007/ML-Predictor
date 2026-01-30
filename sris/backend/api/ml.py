from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from ml.price_predictor import PricePredictor
from ml.demand_forecaster import DemandForecaster
from ml.customer_segmenter import CustomerSegmenter
from ml.anomaly_detector import AnomalyDetector
from ml.recommender import Recommender
import os

router = APIRouter()

DATA_PATH = 'd:/MLAPP/sris/data/retail_data.csv'
CUST_PATH = 'd:/MLAPP/sris/data/customers.csv'
PROD_PATH = 'd:/MLAPP/sris/data/products.csv'

@router.get("/predict/price")
async def predict_price(category: str, current_user: str = Depends(get_current_user)):
    predictor = PricePredictor()
    price = predictor.predict(category)
    if price is None:
        raise HTTPException(status_code=400, detail="Model not trained")
    return {"category": category, "predicted_price": price}

@router.get("/forecast/demand")
async def forecast_demand(category: str, current_user: str = Depends(get_current_user)):
    forecaster = DemandForecaster()
    forecast = forecaster.predict(category)
    if forecast is None:
        raise HTTPException(status_code=400, detail="Model not trained")
    return {"category": category, "forecast": forecast}

@router.get("/recommendations/{customer_id}")
async def get_recommendations(customer_id: int, current_user: str = Depends(get_current_user)):
    rec = Recommender()
    recommendations = rec.get_recommendations(customer_id, DATA_PATH, PROD_PATH)
    return {"customer_id": customer_id, "recommendations": recommendations}

@router.post("/train-all")
async def train_all_models(current_user: str = Depends(get_current_user)):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Data file not found. Generate data first.")
    
    PricePredictor().train(DATA_PATH)
    DemandForecaster().train(DATA_PATH)
    CustomerSegmenter().train(CUST_PATH)
    AnomalyDetector().train(DATA_PATH)
    
    return {"message": "All models trained successfully"}
