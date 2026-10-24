from pydantic import BaseModel

class student(BaseModel):
    id: int
    name: str
    age:int
    password:str


class Login(BaseModel):
    username: str
    password: str