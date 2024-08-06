from typing import List,Optional
from fastapi.params import Body
from fastapi import FastAPI,Response, status,HTTPException,Depends
from datetime import datetime
from pydantic import BaseModel,Field
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models,schemas,utils
from config import settings
from routers import post,user,auth
from database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


    # review:str
while True:

    try:
        conn=psycopg2.connect(host="localhost",database="customer",user="postgres",password="2405",cursor_factory=RealDictCursor)
    # cursor_factory=RealDictCursor this sends the column as the value where as without it it actually sends without column name, sends just the values
        cursor=conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("connection to database is failed")
        print("Error",error)
        time.sleep(2)
