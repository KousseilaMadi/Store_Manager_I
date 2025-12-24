from sqlalchemy import and_, func
from Models.SaleModel import SaleModel
from datetime import date
class SaleRepository:
    
    def add(self, session, sale):
        session.add(sale)
    
    def get(self, session, sale_id):
        return session.get(SaleModel, sale_id)
    
    def get_all(self, session):
        return session.query(SaleModel).all()
    
    def get_filtered(self, session, user_id, start_date=None, end_date=None):
        query = session.query(SaleModel)
        if user_id:
            query = query.filter(SaleModel.user_id == user_id)
            today = date.today()
            query = query.filter(func.date(SaleModel.created_at) == today)
            return query.all()
        if start_date and end_date:
            query = query.filter(and_(SaleModel.created_at <= end_date, SaleModel.created_at >= start_date))
        elif start_date:
            query = query.filter(SaleModel.created_at >= start_date)
        elif end_date:
            query = query.filter(SaleModel.created_at <= end_date)
        
        return query.all()
    
    def delete(self, session, sale):
        session.delete(sale)