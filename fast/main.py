from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import *
import databasemodels
from database import engine, sessionlocal
import jwt
from datetime import datetime, timedelta, timezone
import secrets
from database import get_db

app = FastAPI()

databasemodels.base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return {'message': 'welcome to FastAPI!'}

products = [
    student(id=1, name='John Doe',age=77,password="123"),
    student(id=2, name='Jane Smith',age=99,password="123")
]

@app.get("/students")
def get_students():
    return products

@app.get("/student/id")
def get_one_student(id:int):
    for p in products:
        if p.id == id:
            return p
    return "student not found"

@app.post("/student")
def add_student(p:student):
    products.append(p)
    return products

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


@app.post("/login")
def login(data: Login, db: Session = Depends(get_db)):

    student = db.query(databasemodels.student).filter(
        databasemodels.student.name == data.username
    ).first()

    if student is None or student.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    payload = {
        "id": str(student.id),
        "name": student.name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/studentss/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(databasemodels.student).all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "age": s.age
        }
        for s in students
    ]