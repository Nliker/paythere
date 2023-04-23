import os,sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from expection import DatabaseError

class UserService:
    def __init__(self,user_model,conf):
        self.conf=conf
        self.user_model=user_model

    def set_db(self,db):
        self.user_model.set_db(db)
        return self

    def create_user(self,new_user):
        try:
            print(5/0)
            result=self.user_model.insert_user(new_user)
            
            return result
        except DatabaseError as error_mode:
            raise DatabaseError()