import os,sys
from sql import User
from expection import DatabaseError
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

class UserModel:
    def set_db(self,db):
        self.db=db
    
    def insert_user(self,new_user):
        try:
            new_user=User(
                phone_number=new_user.phone_number,
                hashed_password=new_user.password
            )

            self.db.add(new_user)
            raise DatabaseError()
        except:
            self.db.rollback()
            raise
        else:
            self.db.commit()
            self.db.refresh(new_user)
            print(new_user.__dict__)

            return new_user