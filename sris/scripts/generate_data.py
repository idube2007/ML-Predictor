import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_retail_data(num_records=5000):
    np.random.seed(42)
    
    # 1. Product Data
    products = [
        {'id': i, 'name': f'Product {i}', 'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Groceries', 'Beauty']),
         'base_price': np.random.uniform(10, 500)} for i in range(1, 101)
    ]
    pd_products = pd.DataFrame(products)
    
    # 2. Customer Data
    customers = [
        {'customer_id': i, 'age': np.random.randint(18, 70), 'gender': np.random.choice(['M', 'F', 'Other']),
         'annual_income': np.random.uniform(20000, 150000), 'loyalty_score': np.random.uniform(1, 100)} for i in range(1, 501)
    ]
    pd_customers = pd.DataFrame(customers)
    
    # 3. Sales Data
    start_date = datetime(2023, 1, 1)
    sales = []
    
    for _ in range(num_records):
        cust = pd_customers.sample(1).iloc[0]
        prod = pd_products.sample(1).iloc[0]
        date = start_date + timedelta(days=np.random.randint(0, 365))
        
        # Add some seasonality and price variation
        month_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
        actual_price = prod['base_price'] * month_factor * np.random.uniform(0.9, 1.1)
        quantity = np.random.randint(1, 5)
        
        # Anomaly simulation (rare high quantity or zero price)
        is_anomaly = np.random.random() < 0.01
        if is_anomaly:
            if np.random.random() > 0.5:
                quantity = np.random.randint(20, 50) # Bulk buy anomaly
            else:
                actual_price = actual_price * 0.1 # Price glitch anomaly

        sales.append({
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': int(cust['customer_id']),
            'product_id': int(prod['id']),
            'product_name': prod['name'],
            'category': prod['category'],
            'price': round(actual_price, 2),
            'quantity': quantity,
            'total_amount': round(actual_price * quantity, 2),
            'is_anomaly': is_anomaly
        })
        
    pd_sales = pd.DataFrame(sales)
    
    # Create directory if not exists
    os.makedirs('d:/MLAPP/sris/data', exist_ok=True)
    
    # Save to CSV
    pd_sales.to_csv('d:/MLAPP/sris/data/retail_data.csv', index=False)
    pd_customers.to_csv('d:/MLAPP/sris/data/customers.csv', index=False)
    pd_products.to_csv('d:/MLAPP/sris/data/products.csv', index=False)
    
    print(f"Generated {num_records} sales records.")
    print(f"Data saved to d:/MLAPP/sris/data/")

if __name__ == "__main__":
    generate_retail_data()
