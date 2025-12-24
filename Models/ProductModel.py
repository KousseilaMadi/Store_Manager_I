from sqlalchemy import Column, Integer, String, Float, DateTime
from .Base import Base


class ProductModel(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    stock = Column(Integer, nullable=False, default=1)
    cost_price = Column(Float, nullable=True) # Optional
    created_at = Column(DateTime, nullable=False)