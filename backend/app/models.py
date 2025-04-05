from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum
from enum import Enum as PyEnum

class OrderStatus(str, PyEnum):
    PENDING = "PENDENTE" 
    PROCESSING = "PROCESSANDO" 
    SHIPPED = "ENTREGUE" 
    DELIVERED = "ENVIADO" 
    CANCELLED = "CANCELADO"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    category = Column(String(100), index=True)
    image = Column(String(255))
    rating_rate = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Integer, default=1)
    stock_quantity = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    total = Column(Float, nullable=False)
    customer_email = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )
    shipping_address = Column(Text)
    billing_address = Column(Text)
    payment_method = Column(String(50))
    customer_name = Column(String(255))
    tracking_number = Column(String(100))
    estimated_delivery = Column(DateTime)