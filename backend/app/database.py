import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use variáveis de ambiente para configuração
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./ecommerce.db")

# Para SQLite, precisamos criar o diretório de dados
if DATABASE_URL.startswith("sqlite"):
    os.makedirs(os.path.dirname(DATABASE_URL.split("///")[1]), exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Adicione esta função se não existir
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models import Order, Product  # Importe todos os modelos
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)