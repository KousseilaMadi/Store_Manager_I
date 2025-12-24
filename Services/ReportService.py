from Utilities.Database import session_scope
from Utilities.exceptions import SaleNotFoundError

class ReportService:
    
    def __init__(self, sale_item_repo, sale_repo, product_repo):
        self.sale_item_repo = sale_item_repo
        self.sale_repo = sale_repo
        self.product_repo = product_repo
    
    
    def list_sale_items_grouped_by_sales(self, user_id, start_date=None, end_date=None):
        with session_scope() as session:
            Sales = self.sale_repo.get_filtered(session, user_id, start_date, end_date)
            sales = [{"id":Sale.id, 
                      "total-price": Sale.total_price, 
                      "created-at": Sale.created_at.isoformat() if Sale.created_at else None} for Sale in Sales]
            sales_ids = [sale["id"] for sale in sales]
            Sales_items = self.sale_item_repo.list_by_sales_ids(session, sales_ids)
            sales_items = []
            for Sale_item in Sales_items:
                if Sale_item.product_id:
                    product = self.product_repo.get(session, Sale_item.product_id)
                    sales_items.append({
                        "id":Sale_item.id,
                        "name":product.name,
                        "product-id": Sale_item.product_id,
                        "sale-id":Sale_item.sale_id,
                        "quantity": Sale_item.quantity,
                        "cost-price": product.cost_price,
                        "unit-price": Sale_item.unit_price,
                        "refunded": Sale_item.refunded,
                        "subtotal": Sale_item.subtotal})
                else:
                    sales_items.append({
                        "id":Sale_item.id,
                        "name":Sale_item.old,
                        "product-id": None,
                        "sale-id":Sale_item.sale_id,
                        "quantity": Sale_item.quantity,
                        "cost-price": Sale_item.cost_price,
                        "unit-price": Sale_item.unit_price,
                        "refunded": Sale_item.refunded,
                        "subtotal": Sale_item.subtotal})

            
        grouped = {}
        for sale in sales:
            grouped[sale["id"]] = {
                "sale": sale,
                "items": []
            }
            # {
            #     "sale_id":{
            #         "sale": sale,
            #         "items":[sale items]
            #     },
            # }
        for sale_item in sales_items:
            grouped[sale_item["sale-id"]]["items"].append(sale_item)
        
        return grouped
    
    def calculate_revenue(self, start_date=None, end_date=None):
        grouped = self.list_sale_items_grouped_by_sales(start_date, end_date)
        revenue = 0
        for sale in grouped.values():
            revenue += sale["sale"]["total-price"]
        return revenue

        
    def calculate_profit(self, start_date=None, end_date=None):
        grouped = self.list_sale_items_grouped_by_sales(start_date, end_date)
        cost = 0
        with session_scope() as session:
            products_ids = set()
            for sale in grouped.values():
                for item in sale["items"]:
                    products_ids.add(item["product-id"])
            products_ids = list(products_ids)
            products = self.product_repo.get_by_ids(session, products_ids)
            products_map = {product.id: product for product in products}
            for sale in grouped.values():
                for item in sale["items"]:
                    product = products_map.get(item["product-id"])
                    cost_price = product.cost_price if product else None
                    if cost_price is None:
                        continue
                    cost += cost_price * item["quantity"]
            
        profit = self.calculate_revenue(start_date, end_date) - cost     
        return profit
    
    