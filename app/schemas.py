from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint
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
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    token:str
    token_type:str 

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)

