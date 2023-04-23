import sys,os
from fastapi import Depends,APIRouter
from sql import get_db
from sqlalchemy.orm import Session
from sql import User,Product
from schema import *
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


user_api=APIRouter(prefix="/users",tags=["users"])

def user_router(app,services):
    user_service=services.user_service
    product_service=services.product_service
    
    app.include_router(user_api)

    @user_api.post("/sign_up")
    async def post_sign_up(new_user: UserCreate,db: Session = Depends(get_db)):
        result=user_service.set_db(db).create_user(new_user)
        print(result)

        # result=db.query(User).filter(User.phone_number == phone_number).first()
        # print(result.__dict__)

        return {"data":"good"}

    @user_api.post("/login")
    async def post_login(phone_number: str,password: str):
        return {"data":"good"}