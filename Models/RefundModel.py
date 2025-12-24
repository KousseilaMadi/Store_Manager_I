from sqlalchemy import Column, Integer, DateTime, ForeignKey
from .Base import Base

class RefundModel(Base):
    __tablename__ = 'refunds'
    id = Column(Integer, primary_key=True, nullable=False)
    sale_item_id = Column(Integer, ForeignKey('sale_item.id'), nullable=False)
    quantity_refunded = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)