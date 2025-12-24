from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from Models import SaleItemModel

class SaleModel(Base):
    __tablename__ = 'sales'
    id = Column(Integer, nullable=False, primary_key=True)
    total_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False,)
    created_at = Column(DateTime, nullable=False)
    items = relationship("SaleItemModel", back_populates="sale")