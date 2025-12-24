from datetime import datetime
from Models.RefundModel import RefundModel
from Utilities.Database import session_scope
from Utilities.exceptions import SaleItemNotFoundError, RefundQuantityExceededError, SaleNotFoundError, UserUnmatchError, SaleItemAlreadyRefunded

class RefundService:
    def __init__(self, product_repo, sale_repo, sale_item_repo, refund_repo):
        self.product_repo = product_repo
        self.sale_repo = sale_repo
        self.sale_item_repo = sale_item_repo
        self.refund_repo = refund_repo
    
    def apply_refund(self, sale_item_id, refund_qty=1, restock_qty=1):
        with session_scope() as session:
            sale_item = self.sale_item_repo.get(session, sale_item_id)
            if not sale_item:
                raise SaleItemNotFoundError(sale_item_id)
            sale = self.sale_repo.get(session, sale_item.sale_id)
            if not sale:
                raise SaleNotFoundError(sale_item.sale_id)

            refundable_qty = sale_item.quantity
            
            if refund_qty > (refundable_qty - sale_item.refunded):
                raise SaleItemAlreadyRefunded(sale_item_id)
            refund = RefundModel(sale_item_id=sale_item_id,
                            quantity_refunded=refund_qty,
                            created_at=datetime.now())
            session.add(refund)
            
            sale_item.refunded += refund_qty
            
            if restock_qty > refund_qty:
                raise RefundQuantityExceededError(restock_qty)
            product = self.product_repo.get(session, sale_item.product_id)
            product.stock += restock_qty
        
    def list_refunds(self):
        with session_scope() as session:
            Refunds_list = self.refund_repo.get_all(session)
            refunds_list = [{"id":refund.id,
                             "sale-item-id": refund.sale_item_id,
                             "quantity-refunded": refund.quantity_refunded,
                             "created-at": refund.created_at.isoformat()} for refund in Refunds_list]
            sale_items_ids = [refund.sale_item_id for refund in Refunds_list if refund.sale_item_id is not None]
            sale_items_list = self.sale_item_repo.list_by_ids(session, sale_items_ids)
            
            products_ids = [sale_item.product_id for sale_item in sale_items_list]
            products_list = self.product_repo.get_by_ids(session, products_ids)
            products_map = {product.id: product for product in products_list}

            sale_items_map = {sale_item.id: {'sale-item-id': sale_item.id,
                                             'sale-item-name': products_map[sale_item.product_id].name} for sale_item in sale_items_list}
            
        for refund in refunds_list:
            refund["unit-price"] = sale_items_map.get(refund['sale-item-id'])['sale-item-id']
            refund["name"] = sale_items_map.get(refund['sale-item-id'])['sale-item-name']
        return refunds_list
    
    
    
    
    
    
    