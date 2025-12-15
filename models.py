from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    file: str | None = None
    date_reg: str
    date_born: str
    sex: str 
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode: True