from Models.SaleItemModel import SaleItemModel

class SaleItemRepository:
    
    def add(self, session, saleItem):
        session.add(saleItem)
    
    def get(self, session, saleItem_id):
        return session.get(SaleItemModel, saleItem_id)
    
    def list_sale_items_by_product(self, session, product_id):
        return session.query(SaleItemModel).filter(SaleItemModel.product_id == product_id).all()

    def list_by_sale_id(self, session, sale_id):
        return session.query(SaleItemModel).filter(SaleItemModel.sale_id == sale_id).all()
    
    def list_by_sales_ids(self, session, sales_ids):
        return session.query(SaleItemModel).filter(SaleItemModel.sale_id.in_(sales_ids))
    
    def list_by_ids(self, session, sale_items_ids):
        return session.query(SaleItemModel).filter(SaleItemModel.id.in_(sale_items_ids))

    def delete(self, session, saleItem):
        session.delete(saleItem)