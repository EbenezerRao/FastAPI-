from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List

# ==========================================
# 1. DATABASE SETUP (SQLite)
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./marketplace.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. MODELS (The Database Table)
# ==========================================
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

# Create the table
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. SCHEMAS (The Pydantic Shields)
# ==========================================
class ProductCreate(BaseModel):
    name: str
    price: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True

# ==========================================
# 4. APP & MIDDLEWARE
# ==========================================
app = FastAPI()

# Crucial for React Native to talk to FastAPI without getting blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 5. ROUTES (The Endpoints)
# ==========================================

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products