from fastapi import Depends,APIRouter

product_api=APIRouter(prefix="/products",tags=["products"])

def product_router(app,services):
    app.include_router(product_api)

    @product_api.post("/")
    async def post_product(category: str,net_price: str):
        return {"data":"good"}

    @product_api.put("/{product_id}")
    async def put_product(phone_number: str,password: str):
        return {"data":"good"}