class PhoneNumberLength(Exception):
    status_code=400
    def __str__(self):
        return "please insert 11 length phone number"


class PasswordLength(Exception):
    status_code=400
    def __str__(self):
        return "password should have length between 8 and 16"

class NameKorean(Exception):
    status_code=400
    def __str__(self):
        return "Name should be complete korean"

class CategoryLength(Exception):
    status_code=400
    def __str__(self):
        return "Category should have length under 255"

class NameLength(Exception):
    status_code=400
    def __str__(self):
        return "Name should have length under 255"


class PriceRange(Exception):
    status_code=400
    def __str__(self):
        return "Price should be between 0 and 100000000"

class DescriptionLength(Exception):
    status_code=400
    def __str__(self):
        return "DescriptionLength should have length under 255"

class BarcodeLength(Exception):
    status_code=400
    def __str__(self):
        return "BarcodeLength should be 13 length"
    

class ExpireationDate(Exception):
    status_code=400
    def __str__(self):
        return "ExpireationDate should be under 3000-12-12"
    
    
class Size(Exception):
    status_code=400
    def __str__(self):
        return "Size must be one of small,medium,large"
    
class PhoneNumberType(Exception):
    status_code=400
    def __str__(self):
        return "Phone number should be number"
    
