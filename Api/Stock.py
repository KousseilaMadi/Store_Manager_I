from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from Repositories.ProductRepository import ProductRepository
from Repositories.SaleItemRepository import SaleItemRepository
from Services.StockService import StockService
from Utilities.exceptions import ProductNotFoundError, InvalidInputError, StoreError

class Stock:
    def __init__(self, stock_service):
        self.stock_service = stock_service

    def add_product(self, barcode, name, price, quantity, cost_price):
        try:
            product_id = self.stock_service.add_product(barcode, name, price, quantity, cost_price)
            return {"success": True, "data": {"product_id": product_id}, "message": "Product added !"}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except SQLAlchemyError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
        
    def fetch_products(self, product_name, barcode, start_date, end_date):
        try:
            products = self.stock_service.list_products(product_name, barcode, start_date, end_date)
            return {"success": True, "data":{"products": products}, "message": "products loaded"}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
        except SQLAlchemyError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def edit_product(self, product_id, barcode, name, price, stock, cost_price):
        try:
            product = self.stock_service.update_product(product_id, barcode, name, price, stock, cost_price)
            return {"success": True, "data": product, "message": "Product updated !"}
        except ProductNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except InvalidInputError as e:
            return {"success": False, "error_type": "validation", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def delete_product(self, product_id):
        try:
            product_id = self.stock_service.delete_product(product_id)
            return {"success": True, "data": {"product_id": product_id}, "message": "Product deleted !"}
        except ProductNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}