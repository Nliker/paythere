from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,date

"""
UserInfo->클라이언트에게 보여지는 데이터
User->user의 원본 데이터
"""


class Meta(BaseModel):
    code: int
    message: str
    
class ResponseBase(BaseModel):
    meta: Meta

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
    deleted: bool

class UserInfo(UserBase):
    id: int
    created_at: datetime


class UserResponse(BaseModel):
    user:UserInfo

class UsersResponse(BaseModel):
    users: List[UserInfo]


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
    


    
    


