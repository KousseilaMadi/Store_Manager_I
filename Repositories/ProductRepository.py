from operator import and_
from Models.ProductModel import ProductModel

class ProductRepository:
    
    def add(self, session, product):
        session.add(product)
    
    def get(self, session, product_id):
        return session.get(ProductModel, product_id)
    
    def get_by_name(self, session, product_name):
        return session.query(ProductModel).filter(ProductModel.name == product_name).first()

    def list_by_name(self, session, product_name_pattern):
        return session.query(ProductModel).filter(ProductModel.name.ilike(product_name_pattern)).all()

    def get_by_ids(self, session, products_ids):
        return session.query(ProductModel).filter(ProductModel.id.in_(products_ids)).all()
    
    def get_by_barcode(self, session, barcode):
        return session.query(ProductModel).filter(ProductModel.barcode == barcode).first()
    
    def list_filtered(self, session, product_name, barcode, start_date=None, end_date=None):
        query = session.query(ProductModel)
        if start_date:
            query = query.filter(ProductModel.created_at >= start_date)
        
        if end_date:
            query = query.filter(ProductModel.created_at <= end_date)
        
        if product_name:
            query = query.filter(ProductModel.name.ilike(product_name))
        
        if barcode:
            query = query.filter(ProductModel.barcode.ilike(barcode))
        return query.all()



    
    def delete(self, session, product):
        session.delete(product)