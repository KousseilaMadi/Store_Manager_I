from Models.RefundModel import RefundModel

class RefundRepository:
    
    def add(self, session, refund):
       session.add(refund)
     
    def get(self, session, refund_id):
        return session.get(RefundModel, refund_id)
    
    def get_all(self, session):
        return session.query(RefundModel).all()
    
    def delete(self, session, refund):
        session.delete(refund)