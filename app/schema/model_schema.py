from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,date

class ProductBase(BaseModel):
    user_id: int
    category: str
    net_price: float
    cost_price: float
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    user_id: int
    created_at: date
    
    class Config:
        orm_mode = True


class InsertUser(BaseModel):
    phone_number: str
    hashed_password: str

class PostSignUpUser(BaseModel):
    phone_number: str
    password: str


class GetUser(InsertUser):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool    

    class Config:
        orm_mode = True