import sys,os
from fastapi import Depends,APIRouter,HTTPException
from sql import get_db
from sqlalchemy.orm import Session
from sql import User,Product
from schema import *
from auth import verify_token
import traceback
import expection
import inspect
from response import *

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


user_api=APIRouter(prefix="/users",tags=["users"])

def user_router(app,services):
    user_service=services.user_service
    product_service=services.product_service
    
    app.include_router(user_api)

    @user_api.post("/sign_up")
    async def post_sign_up(new_user: PostSignUpUser,db: Session = Depends(get_db)):
        try:
            phone_number_existance=user_service.set_db(db).is_phone_number_existance(new_user.phone_number)
            if phone_number_existance==False:
                raise expection.PhoneNumberExists()
            
            is_user_deleted=user_service.set_db(db).is_user_deleted_by_phone_number(new_user.phone_number)
            if is_user_deleted==True:
                raise expection.UserWasDeleted()

            created_user_id=user_service.set_db(db).create_new_user(new_user)
            created_user_info=user_service.set_db(db).get_user_info_by_id(created_user_id)

            return make_http_response_json(Created_201,{"user":created_user_info})
        except Exception as es:
            if es.__class__.__name__ in inspect.getmembers(expection): 
                expection.make_http_error(es)
            else:
                print(traceback.format_exc())
                raise HTTPException(status_code=500, detail="Internel Server Error")

    # @user_api.post("/login")
    # async def post_login(phone_number: str,password: str):
    #     try:
    #     except Exception as es:
    #         if es.__class__.__name__ in inspect.getmembers(expection): 
    #             expection.make_http_error(es)
    #         else:
    #             print(traceback.format_exc())
    #             raise HTTPException(status_code=500, detail="Internel Server Error")
    
    # @user_api.get("{user_id}")
    # async def get_user(user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
    #     try:
    #     except Exception as es:
    #         if es.__class__.__name__ in inspect.getmembers(expection): 
    #             expection.make_http_error(es)
    #         else:
    #             print(traceback.format_exc())
    #             raise HTTPException(status_code=500, detail="Internel Server Error")