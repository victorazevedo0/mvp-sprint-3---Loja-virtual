from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..database import SessionLocal
from ..models import Product
import requests
from pydantic import BaseModel
from typing import Optional
from ..database import SessionLocal
from ..models import Product

router = APIRouter()

FAKE_STORE_API = "https://fakestoreapi.com/products"

@router.get("/sync-products/")
def sync_products():
    db = SessionLocal()
    try:
        # Busca produtos da API externa
        response = requests.get(FAKE_STORE_API)
        products = response.json()
        
        # Atualiza o banco de dados
        for product_data in products:
            product = db.query(Product).filter(Product.id == product_data['id']).first()
            
            if product:
                # Atualiza produto existente
                product.title = product_data['title']
                product.price = product_data['price']
                product.description = product_data['description']
                product.category = product_data['category']
                product.image = product_data['image']
                product.rating_rate = product_data['rating']['rate']
                product.rating_count = product_data['rating']['count']
            else:
                # Cria novo produto
                new_product = Product(
                    id=product_data['id'],
                    title=product_data['title'],
                    price=product_data['price'],
                    description=product_data['description'],
                    category=product_data['category'],
                    image=product_data['image'],
                    rating_rate=product_data['rating']['rate'],
                    rating_count=product_data['rating']['count']
                )
                db.add(new_product)
        
        db.commit()
        return {"message": f"{len(products)} produtos sincronizados com sucesso"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/products/")
def get_products(category: str = None):
    db = SessionLocal()
    try:
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        return query.all()
    finally:
        db.close()
        
@router.put("/products/{product_id}")
def update_product(product_id: int, product_data: dict):
    db = SessionLocal()
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        for key, value in product_data.items():
            setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()