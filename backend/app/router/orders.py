from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from ..database import get_db
from .. import models, schemas
from fastapi.routing import APIRoute
from ..models import OrderStatus

class CustomAPIRoute(APIRoute):
    def get_operation_id(self, route: "APIRoute") -> str:
        return f"{self.tags[0]}_{self.name}" if self.tags else self.name

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    route_class=CustomAPIRoute,
    redirect_slashes=False
)

class OrderItemBase(BaseModel):
    product_id: int = Field(..., example=1)
    title: str = Field(..., example="Produto Exemplo")
    price: float = Field(..., gt=0, example=10.99)
    quantity: int = Field(..., gt=0, example=2)

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[OrderItemBase] = Field(..., min_items=1)
    total: float = Field(..., gt=0, example=21.98)
    customer_email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        example="cliente@exemplo.com"
    )
    status: OrderStatus = Field(default=OrderStatus.PENDING, example="PENDENTE")

    class Config:
        from_attributes = True

class OrderResponse(OrderCreate):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")

    class Config:
        from_attributes = True

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_order",
    summary="Cria um novo pedido",
    response_description="Pedido criado com sucesso"
)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para criação de novos pedidos (checkout).
    
    Recebe:
    - Lista de itens (produto, quantidade, preço)
    - Valor total do pedido
    - Email do cliente
    - Status do pedido (opcional, padrão: PENDING)
    """
    try:
        # Validação do valor total
        calculated_total = sum(item.price * item.quantity for item in order.items)
        if not abs(calculated_total - order.total) < 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O total do pedido não corresponde à soma dos itens"
            )

        db_order = models.Order(
            items=[item.model_dump() for item in order.items],
            total=order.total,
            customer_email=order.customer_email,
            status=order.status.upper(),
            created_at=datetime.utcnow()
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar pedido: {str(e)}"
        )

@router.get(
    "/",
    response_model=List[OrderResponse],
    operation_id="list_orders",
    summary="Lista todos os pedidos",
    response_description="Lista de pedidos paginada"
)
async def list_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        return db.query(models.Order)\
               .order_by(models.Order.created_at.desc())\
               .offset(skip)\
               .limit(limit)\
               .all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedidos: {str(e)}"
        )

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    operation_id="get_order",
    summary="Obtém um pedido específico",
    response_description="Detalhes do pedido"
)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        return order
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedido: {str(e)}"
        )

@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    operation_id="update_order",
    summary="Atualiza um pedido existente",
    response_description="Pedido atualizado com sucesso"
)
async def update_order(
    order_id: int,
    order_update: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        
        # Validação do valor total
        calculated_total = sum(item.price * item.quantity for item in order_update.items)
        if not abs(calculated_total - order_update.total) < 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O total do pedido não corresponde à soma dos itens"
            )

        db_order.items = [item.model_dump() for item in order_update.items]
        db_order.total = order_update.total
        db_order.customer_email = order_update.customer_email
        db_order.status = order_update.status.upper()
        
        db.commit()
        db.refresh(db_order)
        return db_order
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar pedido: {str(e)}"
        )

@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_order",
    summary="Remove um pedido",
    response_description="Pedido removido com sucesso"
)
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        
        db.delete(db_order)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir pedido: {str(e)}"
        )