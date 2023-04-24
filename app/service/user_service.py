import os,sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from exception import DatabaseError
from schema import *
import bcrypt
from datetime import datetime,timedelta
import jwt

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
            inserted_user=self.user_model.insert_user(InsertUser(**new_user.dict(),hashed_password=hashed_password))
    
            return inserted_user.id
        except DatabaseError as es:
            raise es
        
    def is_phone_number_exists(self,phone_number: str)->bool:
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
        
    def get_user_credential_by_phone_number(self,phone_number: str)->UserCredential:
        """
            핸드폰 번호를 통해 유저의 정보를 불러옵니다.
        """
        try:
            user_credential=self.user_model.select_user_id_and_password_by_phone_number(phone_number)
            user=UserCredential(**user_credential.dict())
            return user
        except DatabaseError as es:
            raise es

    def check_password(self,hashed_password: str,password: str)->bool:
        """
            비밀번호가 유효한지 확인합니다.
        """
        try:
            authorized=bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))
            return authorized
        except DatabaseError as es:
            raise es
    
    def generate_access_token(self,user_id: int)->str:
        """
            접근토큰을 생성합니다.
        """
        try:
            jwt_expire_time=timedelta(seconds=self.conf.jwt_expire_time)
            utc_time_now=datetime.utcnow()
            access_token_expire=utc_time_now+jwt_expire_time

            payload={
                'user_id':user_id,
                'exp':access_token_expire,
                'iat':utc_time_now
            }

            access_token=jwt.encode(payload,self.conf.jwt_secret_key,'HS256')
            return access_token
        except DatabaseError as es:
            raise es

    def is_user_id_exists(self,user_id: int)->bool:
        """
            유저의 번호가 존재하는지 확인합니다.
        """
        try:
            user=self.user_model.select_user_by_id(user_id)
            if user==None:
                return False
            else:
                return True
        except DatabaseError as es:
            raise es
        
    def is_user_deleted_by_id(self,user_id: int)->bool:
        """
            유저의 번호에 해당하는 유저가 삭제된 기록이 있는지 확인합니다.
        """
        try:
            user=self.user_model.select_user_by_id(user_id)
            if user!=None and user.deleted==True:
                return True
            else:
                return False
        except DatabaseError as es:
            raise es


        
    

        
