import os,sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from exception import DatabaseError
from schema import *
import bcrypt

class UserService:
    def __init__(self,user_model,conf):
        self.conf=conf
        self.user_model=user_model

    def set_db(self,db):
        self.user_model.set_db(db)
        return self

    def create_new_user(self,new_user: CreateUser)->int:
        """
            새로운 회원을 생성합니다.
        """
        try:
            password=new_user.password
            hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            print(type(new_user))
            inserted_user=self.user_model.insert_user(InsertUser(**new_user.dict(),hashed_password=hashed_password))
    
            return inserted_user.id
        except DatabaseError as es:
            raise es
        
    def is_phone_number_existance(self,phone_number: str)->bool:
        """
            핸드폰 번호의 회원이 등록되어 있는가를 확인합니다.
        """
        try:
            user=self.user_model.select_user_by_phone_number(phone_number)
            if user !=None:
                return True
            else:
                return False
        except DatabaseError as es:
            raise es
    
    def is_user_deleted_by_phone_number(self,phone_number: str)->bool:
        """
            핸드폰 번호의 회원이 삭제된 기록이 있는 지를 확인합니다.
        """
        try:
            user=self.user_model.select_user_by_phone_number(phone_number)
            if user!=None and user.deleted==True:
                return True
            else:
                return False
        except DatabaseError as es:
            raise es
    
    def get_user_info_by_id(self,user_id: int)->UserInfo:
        """
            유저의 번호를 통해 유저의 정보를 불러옵니다.
        """
        try:
            user=self.user_model.select_user_by_id(user_id)
            user=UserInfo(**user.dict())
            return user
        except DatabaseError as es:
            raise es
        
        
