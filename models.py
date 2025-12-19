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
    
class UserPatch(BaseModel):
    newUsername: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
        
class FilesBase(BaseModel):
    file: str
    
class FileResponse(FilesBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True