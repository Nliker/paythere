from sqlalchemy import Boolean,Column, Integer, String,DateTime,DECIMAL
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True)
    hashed_password=Column(String)
    updated_at=Column(DateTime)
    created_at=Column(DateTime)
    deleted=Column(Boolean,default=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    user_id=Column(Integer)
    category = Column(String)
    net_price = Column(DECIMAL(10,2))
    cost_price=Column(DECIMAL(10,2))
    name=Column(String)
    description=Column(String)
    barcode=Column(String)
    expiration_date=Column(DateTime)
    size=Column(String)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
    deleted=Column(Boolean,default=False)
    
class ProductInitial(Base):
    __tablename__ = "products_initial"

    product_id = Column(Integer,primary_key=True)
    initial=Column(String)

class Token(Base):
    __tablename__ = "tokens"

    access_token = Column(String,primary_key=True)
