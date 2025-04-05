from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum

class ProductBase(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    rating_rate: Optional[float] = None
    rating_count: Optional[int] = None

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    product_id: int
    title: str
    price: float
    quantity: int

class OrderBase(BaseModel):
    items: List[OrderItem]
    total: float
    customer_email: str
    status: str = "PENDING"
    
class OrderStatus(str, Enum): 
    PENDING = "PENDENTE" 
    PROCESSING = "PROCESSANDO" 
    SHIPPED = "ENTREGUE" 
    DELIVERED = "ENVIADO" 
    CANCELLED = "CANCELADO"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
class OrderResponse(OrderBase):
    id: int
    items: List[dict]
    total: float
    customer_email: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True