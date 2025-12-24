from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .Base import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    CASHIER = "CASHIER"

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, nullable=False)
