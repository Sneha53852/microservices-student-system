from sqlalchemy import Integer,String,Column
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class student(base):
    __tablename__ = "student"
    id= Column(Integer,primary_key = True)
    name=Column(String)
    age= Column(Integer)
    password = Column(String)