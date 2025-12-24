from sqlite3 import IntegrityError
from Repositories.ProductRepository import ProductRepository
from Repositories.SaleRepository import SaleRepository
from Repositories.SaleItemRepository import SaleItemRepository 
from Repositories.RefundRepository import RefundRepository 
from Services.ReportService import ReportService
from Services.RefundService import RefundService
from Utilities.exceptions import RefundQuantityExceededError, SaleItemNotFoundError, SaleNotFoundError, StoreError, UserUnmatchError

class Sales:
    def __init__(self, report_service, refund_service):
        self.report_service = report_service
        self.refund_service = refund_service

    def list_sales(self, user_id, start_date, end_date):
        try:
            sales = self.report_service.list_sale_items_grouped_by_sales(user_id, start_date, end_date)
            return {"success": True, "data":{"sales": sales}, "message":"Fetched sales !"}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def list_refunds(self):
        try:
            refunds = self.refund_service.list_refunds()
            return {"success": True, "data":{"refunds": refunds}, "message":"Fetched refunds !"}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}

    def refund_item(self, sale_item_id, refund_qty=1, restock_qty=1):
        try:
            self.refund_service.apply_refund(sale_item_id, refund_qty, restock_qty)
            return {"success":True, "data":{}, "message":"Refund applied !"}
        except SaleItemNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except SaleNotFoundError as e:
            return {"success": False, "error_type": "existance", "message": str(e)}
        except UserUnmatchError as e:
            return {"success": False, "error_type": "unmatch", "message": str(e)}
        except RefundQuantityExceededError as e:
            return {"success": False, "error_type": "excess", "message": str(e)}
        except IntegrityError as e:
            return {"success": False, "error_type": "database", "message": str(e)}
        except StoreError as e:
            return {"success": False, "error_type": "store_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error_type": "unknown", "message": str(e)}