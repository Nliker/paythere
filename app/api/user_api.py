from fastapi import Depends,APIRouter

user_api=APIRouter(prefix="/users",tags=["users"])

def user_router(app,services):
    app.include_router(user_api)
    
    @user_api.post("/sign_up")
    async def post_sign_up(phone_number: str,password: str):
        return {"data":"good"}

    @user_api.post("/login")
    async def post_login(phone_number: str,password: str):
        return {"data":"good"}