from sqlite3 import IntegrityError
from Repositories.ProductRepository import ProductRepository
from Repositories.UserRepository import UserRepository
from Services.AuthService import AuthService
from Services.RegisterService import RegisterService
from Utilities.exceptions import EmptyRegisterError, InsufficientStockError, ProductNotFoundError, RegisterNotFoundError, StoreError

class Register:
    def __init__(self, auth_service, register_service):
        self.auth_service = auth_service
        self.register_service = register_service

    def add_item(self, register_id, item_id, barcode, qty=1):
        try:
            item = self.register_service.add_item(register_id, item_id, barcode, qty)
            return {"success": True, "data":{"item": item}, "message": "Item Added !"}
        except RegisterNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def add_divers(self, register_id, item_id, price, subtotal, qty=1):
        try:
            self.register_service.add_divers_item(register_id=register_id,
                                                  item_id=item_id,
                                                  price=price,
                                                  subtotal=subtotal,
                                                  qty=qty)
            return {"success": True, "data": {}, "message":"Divers item Added !"}
        except RegisterNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
        


    def search_product(self, product_name):
        try:
            products = self.register_service.list_products_by_name(product_name)
            return {"success": True, "data": products, "message": "Fetched Products !"}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}



    def clear_register(self, register_id):
        self.register_service.clear_register(register_id)

    def checkout(self, register_id):
        try:
            sale_id = self.register_service.checkout(register_id)
            return {"success": True, "data": {"sale_id": sale_id}, "message": "Checkout !"}
        except RegisterNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except EmptyRegisterError as e:
            return {"success": False, "error_type": "empty", "message": str(e)}
        except ProductNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except InsufficientStockError as e:
            return {"success": False, "error_type": "stock", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
    
    def new_register(self):
        try:
            register_id = self.register_service.create_register()
            return {"success": True, "data": {"register_id": register_id}, "message": "New register !"}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
        
    def apply_quantity(self, register_id, item_id, qty):
        try:
            self.register_service.update_item(register_id, item_id, qty)
            return {"success": True, "data": {}, "message": "Quantity applied !"}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
        
    def remove_item(self, register_id, item_id):
        try:
            self.register_service.remove_item(register_id, item_id)
            return {"success": True, "data": {}, "message": "Item removed !"}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}
    

    def calculate_total(self, register_id):
        try:
            total = self.register_service.calculate_total(register_id)
            return {"success": True, "data": {'total': total}, "message": "Total !"}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}