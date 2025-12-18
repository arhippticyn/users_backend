from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str
    file: str | None = None
    date_reg: str
    date_born: date
    sex: str 
    age: int
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True