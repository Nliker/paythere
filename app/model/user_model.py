import os,sys
import sql
from exception import DatabaseError
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import traceback
from schema import *

class UserModel:
    def set_db(self,db):
        self.db=db
    
    def insert_user(self,new_user: InsertUser)->User:
        """
            새로운 유저의 정보를 삽입합니다.
        """
        try:
            new_user=sql.User(
                **new_user.dict()
            )
            self.db.add(new_user)
        except:
            self.db.rollback()
            raise DatabaseError()
        else:
            self.db.commit()
            self.db.refresh(new_user)
            new_user=User(**new_user.__dict__)
            return new_user
        
    def select_user_by_phone_number(self,phone_number: str)->User:
        """
            핸드폰 번호를 가진 유저를 조회합니다.
        """
        try:
            user=self.db.query(sql.User).filter(sql.User.phone_number==phone_number).first()
        except:
            raise DatabaseError()
        else:
            if user!=None:
                user=User(**user.__dict__)
            return user

    def select_user_by_id(self,user_id: int)->User:
        """
            유저 번호와 일치하는 유저를 조회합니다.
        """
        try:
            user=self.db.query(sql.User).filter(sql.User.id==user_id).first()
        except:
            raise DatabaseError()
        else:
            if user!=None:
                user=User(**user.__dict__)
            return user
        
        
    def select_user_id_and_password_by_phone_number(self,phone_number: str)->UserCredential:
        try:
            user=self.db.query(sql.User).filter(sql.User.phone_number==phone_number).first()
        except:
            raise DatabaseError()
        else:
            if user!=None:
                user=UserCredential(**user.__dict__)
            return user
    