from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .Base import Base
from Models import SaleModel

class SaleItemModel(Base):
    __tablename__ = 'sale_item'
    id = Column(Integer, nullable=False, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False) # quantity * unit_price
    refunded = Column(Integer, nullable=False, default=0)
    old = Column(String, nullable=True, default=None)
    cost_price = Column(Float, nullable=True, default=None)
    sale = relationship("SaleModel", back_populates="items")
    