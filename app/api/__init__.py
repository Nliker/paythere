from .user_api import user_router
from .product_api import product_router
from .search_api import search_router

__all__=[
    "user_router",
    "product_router",
    "search_router"
]