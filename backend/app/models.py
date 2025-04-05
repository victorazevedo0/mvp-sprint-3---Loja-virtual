from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum
from enum import Enum as PyEnum

# Enum para status do pedido (opcional, mas recomendado)
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
    category = Column(String(100), index=True)  # Adicionado index para melhor performance em buscas
    image = Column(String(255))
    rating_rate = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # Adicionado campos de status e estoque (opcional)
    is_active = Column(Integer, default=1)  # 1 para ativo, 0 para inativo
    stock_quantity = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    total = Column(Float, nullable=False)
    customer_email = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    # Usando Enum para status (opcional)
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )
    # Adicionado campos adicionais para pedidos
    shipping_address = Column(Text)
    billing_address = Column(Text)
    payment_method = Column(String(50))
    customer_name = Column(String(255))
    # Campos para rastreamento
    tracking_number = Column(String(100))
    estimated_delivery = Column(DateTime)