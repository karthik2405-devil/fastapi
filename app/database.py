from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings

# SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-address/hostman>/<database_name>' 
# format of a connection string to attach the sqlalchemy orm to postgressql

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



