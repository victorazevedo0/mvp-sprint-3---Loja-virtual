from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import Base
from app.router import orders
from app.router.orders import router as orders_router
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(orders.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Backend Online"}


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

