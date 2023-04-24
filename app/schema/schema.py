from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,date
from decimal import Decimal
"""
UserInfo->클라이언트에게 보여지는 데이터
User->user의 원본 데이터
CreateUser->회원을 생성하기 위해 받는 데이터
InsertUser->DB에 저장을 하기 위한 데이터
"""


class Meta(BaseModel):
    code: int
    message: str
    
class ResponseBase(BaseModel):
    meta: Meta

class UserBase(BaseModel):
    phone_number: str


class ProductBase(BaseModel):
    category: str
    net_price: Decimal
    cost_price: Decimal
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: str

class Product(ProductBase):
    id: int
    user_id: int
    updated_at: datetime | None
    created_at: datetime
    deleted: bool

class InsertProduct(ProductBase):
    user_id: int

class CreateProduct(ProductBase):
    category: str
    net_price: Decimal
    cost_price: Decimal
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: str

class UpdateProduct(BaseModel):
    category: Optional[str]
    net_price: Optional[Decimal]
    cost_price: Optional[Decimal]
    name: Optional[str]
    description: Optional[str]
    barcode: Optional[str]
    expiration_date: Optional[date]
    size: Optional[str]

class ProductInfo(ProductBase):
    id: int
    created_at: datetime
    
class UpdatedProductInfo(ProductInfo):
    updated_at: datetime

class InsertUser(UserBase):
    hashed_password: str


class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int
    updated_at: datetime | None
    created_at: datetime
    deleted: bool

class UserInfo(UserBase):
    id: int
    created_at: datetime


class UserResponse(BaseModel):
    user:UserInfo

class UsersResponse(BaseModel):
    users: List[UserInfo]


class ProductResponse(BaseModel):
    product: ProductInfo

class ProductsResponse(BaseModel):
    products: List[ProductInfo]

class UpdatedProductResponse(BaseModel):
    product: UpdatedProductInfo


class UserCredential(InsertUser):
    id: int

class AccessToken(BaseModel):
    access_token: str  



class PostSignUpResponse(ResponseBase):
    data: UserResponse | None
    
class PostLoginResponse(ResponseBase):  
    data: AccessToken | None

class GetUserResponse(ResponseBase):
    data: UserResponse | None


class PostProductResponse(ResponseBase):
    data: ProductResponse | None

class PutProductResponse(ResponseBase):
    data: UpdatedProductResponse | None

class GetProductResponse(ResponseBase):
    data: ProductResponse | None

class GetProductsResponse(ResponseBase):
    data: ProductsResponse | None
    
class DeleteProductResponse(ResponseBase):
    data: str | None




