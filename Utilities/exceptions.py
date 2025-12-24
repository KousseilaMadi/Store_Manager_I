class StoreError(Exception):
    def __init__(self, message):
        if message is None:
            message = "Unknown store error."
        super().__init__(message)
    
class ProductNotFoundError(StoreError):
    def __init__(self, identification_method, identifier):
        message = f"Product with {identification_method} {identifier} was not found."
        super().__init__(message)

        
class RegisterNotFoundError(StoreError):
    def __init__(self, register_id):
        message = f"Register with id {register_id} was not found."
        super().__init__(message)

class RefundQuantityExceededError(StoreError):
    def __init__(self, qty):
        message = f"Refund quantity ({qty}), exceeds purchased amount."
        super().__init__(message)
    
class InvalidInputError(StoreError):
    def __init__(self, ):
        message = f"Input invalid."
        super().__init__(message)

class DatabaseError(StoreError):
    def __init__(self, ):
        message = f"Something wrong with the database."
        super().__init__(message)

class SaleNotFoundError(StoreError):
    def __init__(self, sale_id):
        message = f"Sale with id {sale_id} was not found."
        super().__init__(message)

class SaleItemNotFoundError(StoreError):
    def __init__(self, sale_item_id):
        message = f"Sale Item with id {sale_item_id} was not found."
        super().__init__(message)

class RefundNotFoundError(StoreError):
    def __init__(self, refund_id):
        message = f"Refund with id {refund_id} was not found."
        super().__init__(message)

class EmptyRegisterError(StoreError):
    def __init__(self, register_id):
        message = f"Register with id {register_id} is empty."
        super().__init__(message)

class InsufficientStockError(StoreError):
    def __init__(self, product_id, requested_qty, available_qty):
        message = f"Insufficient stock for product with id {product_id}. Requested: {requested_qty}, Available: {available_qty}."
        super().__init__(message)

class InvalidInputError(StoreError):
    def __init__(self, message):
        super().__init__(message)

class IncorrectPasswordError(StoreError):
    def __init__(self, message):
        super().__init__(message)

class UserNotFoundError(StoreError):
    def __init__(self, username):
        message = f"User with username: {username} does not exist."
        super().__init__(message)

class RequireAdminAccessError(StoreError):
    def __init__(self):
        message = f"Admin access required."
        super().__init__(message)

class InvalidUsernameError(StoreError):
    def __init__(self, message):
        super().__init__(message)

class InvalidPasswordError(StoreError):
    def __init__(self, message):
        super().__init__(message)

class UserUnmatchError(StoreError):
    def __init__(self, message):
        super().__init__(message)

class SaleItemAlreadyRefunded(StoreError):
    def __init__(self, message):
        super().__init__(message)
