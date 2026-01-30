import pandas as pd
import numpy as np

class Recommender:
    def __init__(self):
        pass

    def get_recommendations(self, customer_id, sales_path, products_path):
        sales_df = pd.read_csv(sales_path)
        products_df = pd.read_csv(products_path)
        
        # Simple Logic: Recommend popular products in categories the user hasn't bought high volume of, 
        # or just popular products if no history.
        cust_sales = sales_df[sales_df['customer_id'] == customer_id]
        
        if cust_sales.empty:
            # Recommend top 5 overall
            recommendations = products_df.sample(5).to_dict(orient='records')
        else:
            fav_category = cust_sales['category'].mode()[0]
            # Recommend from fav category that hasn't been bought yet
            bought_ids = cust_sales['product_id'].unique()
            recommendations = products_df[(products_df['category'] == fav_category) & (~products_df['product_id'].isin(bought_ids))].head(5).to_dict(orient='records')
            
            if not recommendations:
                recommendations = products_df.sample(5).to_dict(orient='records')
                
        return recommendations
