import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import exception
import tool
import datetime

def validate_user_auth(data: dict):
    "항상 있는 필드 내에서 검사하기 위해 items사용"
    for key, val in data.items():
        if val==None:
            continue

        if key=="phone_number":
            if len(val)!=11:
                raise exception.PhoneNumberLength()
            if val.isdecimal()==False:
                raise exception.PhoneNumberType()
            

        if key=="password":
            if len(val)<8 or len(val)>16:
                raise exception.PasswordLength()


def validate_create_product(data):
    for key, val in data.items():
        if val==None:
            continue
        
        if key=="category":
            if len(val)>255:
                raise exception.CategoryLength()
            
        if key=="net_price":
            if val>100000000 or val<0:
                raise exception.PriceRange()

        if key=="cost_price":
            if val>100000000 or val<0:
                raise exception.PriceRange()

        if key=="name":
            if len(val)>255:
                raise exception.NameLength()
            if tool.korean_check(val)==False:
                raise exception.NameKorean()

        if key=="description":
            if len(val)>255:
                raise exception.DescriptionLength()

        if key=="barcode":
            if len(val)!=13:
                raise exception.BarcodeLength()

        if key=="expiration_date":
            print(val)
            print(type(val))
            if val>datetime.date(3000,12,12):
                raise exception.ExpireationDate()

        if key=="size":
            if val not in ["small","medium","large"]:
                raise exception.Size()
