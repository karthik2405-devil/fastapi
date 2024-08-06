from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass 
class PostUpdate(PostBase):
    pass 

class Post(BaseModel):
    id: int
    title:str
    content:str
    published:bool
    owner_id:int
    owner:UserOut

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token:str
    token_type:str 

class TokenData(BaseModel):
    id: Optional[str] = None


