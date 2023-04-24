from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,date

class PostSignUpUser(BaseModel):
    phone_number: str
    password: str