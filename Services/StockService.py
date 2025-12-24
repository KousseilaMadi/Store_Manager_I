from datetime import datetime

from Models.ProductModel import ProductModel
from Utilities.Database import session_scope
from Utilities.exceptions import ProductNotFoundError, InvalidInputError

class StockService:
    def __init__(self, product_repo, sale_item_repo):
        self.product_repo = product_repo
        self.sale_item_repo = sale_item_repo
    
    def add_product(self, barcode, name, price, stock, cost_price):
        if name is None or name == "":
            raise InvalidInputError("name cannot be empty.")
        if barcode is None or barcode == "":
            raise InvalidInputError("barcode cannot be empty.")
        if price is None or float(price) < 0:
            raise InvalidInputError("price cannot be negative.")
        if stock is None or int(stock) < 0:
            raise InvalidInputError("stock cannot be negative.")
        if float(cost_price) < 0:
            raise InvalidInputError("cost price cannot be negative.")
            
        product = ProductModel(
            barcode=barcode,
            name=name,
            price=price,
            stock=stock,
            cost_price=cost_price,
            created_at=datetime.now())
        with session_scope() as session:
            self.product_repo.add(session, product)
            session.flush()
            product_id = product.id
        return product_id
    
    def list_products(self, product_name=None, barcode=None, start_date=None, end_date=None):
        if product_name:
            product_name = '%' + product_name + '%'
        if barcode:
            barcode = '%' + barcode + '%'
        with session_scope() as session:
            Products = self.product_repo.list_filtered(session, product_name, barcode, start_date, end_date)
            products = [{"id": p.id,
                         "barcode": p.barcode,
                         "name": p.name,
                         "price": p.price,
                         "stock": p.stock,
                         "cost-price": p.cost_price,
                         "created-at": p.created_at.isoformat() } for p in Products]
        return products

    def update_product(self, product_id, barcode, name, price, stock, cost_price):
        with session_scope() as session:
            product = self.product_repo.get(session, product_id)
            if product is None:
                raise ProductNotFoundError("id", product_id)
            if name is None or name == "":
                raise InvalidInputError("name cannot be empty.")
            if barcode is None or barcode == "":
                raise InvalidInputError("barcode cannot be empty.")
            if price is None or float(price) < 0:
                raise InvalidInputError("price cannot be negative.")
            if stock is None or int(stock) < 0:
                raise InvalidInputError("stock cannot be negative.")
            if float(cost_price) < 0:
                raise InvalidInputError("cost price cannot be negative.")
            
            
            product.barcode = barcode
            product.name = name
            product.price = price
            product.stock = stock
            product.cost_price = cost_price
            
        product = {
            "barcode": barcode,
            "name": name,
            "price": price,
            "stock": stock,
            "cost-price": cost_price
        }
        return product
            
    def delete_product(self, product_id):
        with session_scope() as session:
            product = self.product_repo.get(session, product_id)
            if product is None:
                raise ProductNotFoundError("id", product_id)
            sale_items_list = self.sale_item_repo.list_sale_items_by_product(session, product_id)
            for sale_item in sale_items_list:
                sale_item.old = product.name
                sale_item.product_id = None
                sale_item.cost_price = product.cost_price
            self.product_repo.delete(session, product)
        return product_id