from datetime import datetime
from Utilities.Database import session_scope
from Models.SaleItemModel import SaleItemModel
from Models.SaleModel import SaleModel
from Utilities.exceptions import RegisterNotFoundError, ProductNotFoundError, EmptyRegisterError, InsufficientStockError

class RegisterService:
    def __init__(self, product_repo, auth_service):
        self.registers = {"register-1":[]} #key: register-id, value:scanned_products
        self.product_repo = product_repo
        self.auth_service = auth_service
    
    def create_register(self):
        register_count = len(self.registers)
        num = register_count + 1
        register_id = 'register-' + str(num)
        self.registers[register_id] = []
        return register_id

    def remove_register(self, register_id):
        if register_id in self.registers:
            self.registers.pop(register_id)
        else:
            raise RegisterNotFoundError(register_id)
    
    def get_item_id(self, barcode):
        with session_scope() as session:
            product = self.product_repo.get_by_barcode(session, barcode)
            if product is None:
                raise ProductNotFoundError("barcode", barcode)
            product_id = product.id
        return product_id
    
    def list_products_by_name(self, product_name):
        if product_name is None or product_name.strip() == "":
            product_name_pattern = "%" 
        else:
            product_name_pattern = f"%{product_name.strip()}%" 
        with session_scope() as session:
            products = self.product_repo.list_by_name(session, product_name_pattern)
            products_obj = [{"product-id":p.id,
                             "barcode":p.barcode,
                             "stock": p.stock,
                             "price": p.price} for p in products]
        return products_obj

    def add_item(self, register_id, item_id, barcode, qty=1):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        with session_scope() as session:
            product = self.product_repo.get_by_barcode(session, barcode)
            if product is None:
                raise ProductNotFoundError("barcode", barcode)
            item_obj = {
                "id": item_id,
                "product-id": product.id,
                "name": product.name,
                "price": product.price,
                "qty": 1,
                "subtotal": product.price
            }
            print(items)
        for item in items:
            if item["product-id"] == product.id:
                item["qty"] = item['qty'] + qty
                item["subtotal"] = item_obj['price'] * qty
                return item_obj
        print(qty)
        items.append(item_obj)
        return item_obj

    def add_divers_item(self, register_id, item_id, price, subtotal, qty=1):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        items.append({
            "id": item_id,
            "product-id": None,
            "qty": qty,
            "price": price,
            "subtotal": subtotal
        })
    
    def update_item(self, register_id, item_id, qty):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        for item in items:
            if item["id"] == item_id:
                item["qty"] = qty
                return
    
    def remove_item(self, register_id, item_id):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        for i, item in enumerate(items):
            if item["id"] == item_id:
                items.pop(i)
                return
    
    def clear_register(self, register_id):
        self.registers[register_id] = []
    
    def calculate_total(self, register_id):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        total = 0
        for item in items:
            total += item["price"] * item["qty"]
        return total
    
    def print_receipt(self, sale_id):
        print("printing receipt...")
        
    def checkout(self, register_id):
        items = self.registers.get(register_id)
        if items is None:
            raise RegisterNotFoundError(register_id)
        
        if len(items) == 0:
            raise EmptyRegisterError(register_id)
        
        regular_items = [item for item in items if item.get('product-id')]
        divers_items = [item for item in items if not item.get('product-id')]

        products_ids = [item["product-id"] for item in regular_items]
        with session_scope() as session:
            if products_ids:
                products = self.product_repo.get_by_ids(session, products_ids)
                product_map = {p.id: p for p in products}
            
                for item in regular_items:
                    product = product_map.get(item["product-id"])
                    if product is None:
                        raise ProductNotFoundError('product-id', item["product-id"])
                    if item["qty"] > product.stock:
                        raise InsufficientStockError(product.id, item["qty"], product.stock)
                    
                for item in regular_items:
                    product = product_map.get(item["product-id"])
                    product.stock -= item["qty"]
                    session.add(product)
            
            total = self.calculate_total(register_id=register_id)
            sale = SaleModel(total_price=total,
                            user_id=self.auth_service.current_user['id'],
                            created_at=datetime.now())
            
            session.add(sale)
            session.flush()

            for item in regular_items:
                product = product_map.get(item["product-id"])
                sale_item = SaleItemModel(
                    sale_id=sale.id, 
                    product_id=product.id,
                    quantity=item["qty"],
                    unit_price=product.price,
                    subtotal=item["subtotal"]
                    )
                session.add(sale_item)

            for item in divers_items:
                sale_item = SaleItemModel(
                    sale_id=sale.id,
                    product_id=None,
                    quantity=item["qty"],
                    unit_price=item["price"],
                    subtotal=item["subtotal"]
                    )
                session.add(sale_item)
            
        self.clear_register(register_id)
        self.print_receipt(sale.id)
        return sale.id