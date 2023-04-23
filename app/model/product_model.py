import os,sys
from sql import Product

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

class ProductModel:

    def insert_user(self,new_Product,db):
        return True