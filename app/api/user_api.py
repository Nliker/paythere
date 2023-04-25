import sys,os
from fastapi import Depends,APIRouter,Response
from sql import get_db
from sqlalchemy.orm import Session
from schema import *
from auth import verify_token
import traceback
import exception
from response import *
from validation import *

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


user_api=APIRouter(prefix="/users",tags=["users"])

def user_router(app,services):
    user_service=services.user_service
    
    app.include_router(user_api)

    @user_api.post("/sign_up",status_code=Created_201.status_code,response_model=PostSignUpResponse)
    async def post_sign_up(response: Response,new_user: CreateUser,db: Session = Depends(get_db)):
        """
            회원가입을 합니다.
        """
        try:
            validate_user_auth(new_user.dict())
            phone_number_existance=user_service.set_db(db).is_phone_number_exists(new_user.phone_number)
            if phone_number_existance==True:
                raise exception.PhoneNumberExists()
            
            is_user_deleted=user_service.set_db(db).is_user_deleted_by_phone_number(new_user.phone_number)
            if is_user_deleted==True:
                raise exception.UserWasDeleted()

            created_user_id=user_service.set_db(db).create_new_user(new_user)
            created_user_info=user_service.set_db(db).get_user_info_by_id(created_user_id)

            return make_http_response_json(Created_201,{"user":created_user_info})
        except Exception as es:
            if exception.exceptions_dict.get(es.__class__.__name__,False):
                response.status_code=es.status_code
                return exception.make_http_error(es.status_code,es.__str__())
            else:
                print(traceback.format_exc())
                response.status_code=500
                return exception.make_http_error(500,es.__str__())

    @user_api.post("/login",status_code=Created_201.status_code,response_model=PostLoginResponse)
    async def post_login(response: Response,credential: CreateUser,db: Session = Depends(get_db)):
        """
            로그인을 합니다.
        """
        try:
            validate_user_auth(credential.dict())
            phone_number_existance=user_service.set_db(db).is_phone_number_exists(credential.phone_number)
            if phone_number_existance==False:
                raise exception.PhoneNumberNotExists()

            user_credential=user_service.set_db(db).get_user_credential_by_phone_number(credential.phone_number)

            password_authorized=user_service.set_db(db).check_password(user_credential.hashed_password,credential.password)
            if password_authorized==False:
                raise exception.PasswordNotAuthorized()

            access_token=user_service.set_db(db).generate_access_token(user_credential.id)
            result=user_service.set_db(db).user_login(access_token)

            return make_http_response_json(Created_201,{"access_token":access_token})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())
                
    @user_api.post("/logout",status_code=Created_201.status_code,response_model=PostLogoutResponse)
    async def post_login(response: Response,credentials: dict = Depends(verify_token),db: Session = Depends(get_db)):
        """
            로그인을 합니다.
        """
        try:
            access_token=credentials["access_token"]

            access_token_logouted=user_service.set_db(db).is_user_access_token_logouted(access_token)
            if access_token_logouted==True:
                raise exception.UserLogouted()

            result=user_service.set_db(db).user_logout(access_token)
            

            return make_http_response_json(Created_201,f"User logouted successfully")
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())
    
    @user_api.get("/my",status_code=Get_200.status_code,response_model=GetUserResponse)
    async def get_my(response: Response,credentials: dict = Depends(verify_token),db: Session = Depends(get_db)):
        """
            자신의 정보를 조회합니다.
        """
        try:
            current_user_id=credentials["current_user_id"]
            access_token=credentials["access_token"]
            
            access_token_logouted=user_service.set_db(db).is_user_access_token_logouted(access_token)
            if access_token_logouted==True:
                raise exception.UserLogouted()

            user_existance=user_service.set_db(db).is_user_id_exists(current_user_id)
            if user_existance==False:
                raise exception.UserIdNotExists()
            user_deleted=user_service.set_db(db).is_user_deleted_by_id(current_user_id)
            if user_deleted==True:
                raise exception.UserWasDeleted()

            user_info=user_service.set_db(db).get_user_info_by_id(current_user_id)

            return make_http_response_json(Get_200,{"user":user_info})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())