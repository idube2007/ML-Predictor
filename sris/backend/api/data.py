from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
import pandas as pd
import io
import os
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import Sale, Customer, Product, get_db
from utils.auth import get_current_user

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...), 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        try:
            # Try UTF-8 first
            df = pd.read_csv(io.BytesIO(contents))
        except UnicodeDecodeError:
            # Fallback to Latin-1 for common retail symbols like £
            df = pd.read_csv(io.BytesIO(contents), encoding='latin-1')
        
        count = 0
        cols = [c.lower() for c in df.columns]
        
        # Simple logic to determine which table to populate based on columns
        if 'total_amount' in cols or 'revenue' in cols:
            # Sales data
            for _, row in df.iterrows():
                # Map case-insensitively
                data_row = {k.lower(): v for k, v in row.to_dict().items()}
                
                # Intelligent mapping for common variations
                total = float(data_row.get('total_amount', data_row.get('revenue', 0)))
                qty = int(data_row.get('quantity', 1))
                price = float(data_row.get('price', total / qty if qty > 0 else 0))
                
                sale = Sale(
                    date=pd.to_datetime(data_row.get('date', datetime.utcnow())),
                    customer_id=str(data_row.get('customer_id', '0')),
                    product_id=str(data_row.get('product_id', data_row.get('order_id', '0'))),
                    product_name=str(data_row.get('product_name', 'Unknown')),
                    category=str(data_row.get('category', 'General')),
                    price=price,
                    quantity=qty,
                    total_amount=total,
                    is_anomaly=bool(data_row.get('is_anomaly', False))
                )
                db.add(sale)
                count += 1
        elif 'annual_income' in cols:
            # Customer data
            for _, row in df.iterrows():
                data_row = {k.lower(): v for k, v in row.to_dict().items()}
                cust = Customer(
                    customer_id=str(data_row['customer_id']),
                    age=int(data_row['age']),
                    gender=str(data_row['gender']),
                    annual_income=float(data_row['annual_income']),
                    loyalty_score=float(data_row['loyalty_score'])
                )
                db.add(cust)
                count += 1
        elif 'base_price' in cols:
            # Product data
            for _, row in df.iterrows():
                data_row = {k.lower(): v for k, v in row.to_dict().items()}
                prod = Product(
                    product_id=str(data_row.get('product_id', data_row.get('id', '0'))),
                    name=str(data_row['name']),
                    category=str(data_row['category']),
                    base_price=float(data_row['base_price'])
                )
                db.add(prod)
                count += 1
        else:
            return {"error": f"Invalid CSV format. Request columns not found. Found: {list(df.columns)}"}
        
        db.commit()
        return {"message": f"Successfully processed {count} records"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to process CSV: {str(e)}"}

@router.get("/summary")
async def get_data_summary(db: Session = Depends(get_db)):
    sales_count = db.query(Sale).count()
    customer_count = db.query(Customer).count()
    product_count = db.query(Product).count()
    
    return {
        "sales_records": sales_count,
        "customers": customer_count,
        "products": product_count
    }
