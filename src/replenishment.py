import pandas as pd
import numpy as np
from typing import Dict, List

class InventoryManager:
    def __init__(self, demand_forecast: pd.DataFrame, current_inventory: Dict, lead_time: int = 7, service_level: float = 0.95):
        """
        Initialize inventory manager with:
        - demand_forecast: DataFrame with date and predicted demand
        - current_inventory: Dictionary of {product_id: current_stock}
        - lead_time: Supplier lead time in days
        - service_level: Desired service level (0-1)
        """
        self.forecast = demand_forecast
        self.inventory = current_inventory
        self.lead_time = lead_time
        self.service_level = service_level
        
    def calculate_safety_stock(self, demand_std: float) -> float:
        """Calculate safety stock based on service level"""
        # Z-score for service level (simplified)
        z_score = 1.96  # for 95% service level
        return z_score * demand_std * np.sqrt(self.lead_time)
    
    def calculate_eoq(self, annual_demand: float, ordering_cost: float, holding_cost: float) -> float:
        """Calculate Economic Order Quantity"""
        return np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    
    def generate_replenishment_orders(self, product_id: str, daily_demand_mean: float, daily_demand_std: float) -> Dict:
        """Generate replenishment recommendations for a product"""
        safety_stock = self.calculate_safety_stock(daily_demand_std)
        lead_time_demand = daily_demand_mean * self.lead_time
        reorder_point = lead_time_demand + safety_stock
        
        current_stock = self.inventory.get(product_id, 0)
        
        order_quantity = max(0, reorder_point - current_stock)
        
        return {
            'product_id': product_id,
            'current_stock': current_stock,
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'recommended_order': order_quantity,
            'needs_replenishment': current_stock < reorder_point
        }
    
    def simulate_stock_movement(self, product_id: str, orders: List[Dict], sales_data: pd.DataFrame) -> pd.DataFrame:
        """Simulate inventory movements based on orders and sales"""
        inventory_log = []
        current_stock = self.inventory.get(product_id, 0)
        
        for date, row in sales_data.iterrows():
            # Process sales
            daily_sales = row.get('Sales', 0)
            current_stock -= daily_sales
            current_stock = max(0, current_stock)  # Prevent negative inventory
            
            # Process incoming orders
            for order in orders:
                if order['arrival_date'] == date:
                    current_stock += order['quantity']
            
            inventory_log.append({
                'date': date,
                'stock_level': current_stock,
                'sales': daily_sales
            })
        
        return pd.DataFrame(inventory_log)
