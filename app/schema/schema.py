from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,date

"""
UserInfo->service에서 api로 나가는 데이터 형식
User->model에서 불러온 데이터형식
"""

class UserBase(BaseModel):
    phone_number: str



class InsertUser(UserBase):
    hashed_password: str

class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int
    updated_at: datetime | None
    created_at: datetime
    deleted: datetime

class UserInfo(UserBase):
    id: int
    created_at: datetime



class UserResponse(BaseModel):
    user:UserInfo

class UsersResponse(BaseModel):
    users: List[UserInfo]

class Meta(BaseModel):
    code: int
    message: str


class ResponseBase(BaseModel):
    meta: Meta


class PostSignUpResponse(ResponseBase):
    data: UserResponse | None


    
