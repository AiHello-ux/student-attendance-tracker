from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
from fastapi import Header
from pydantic import BaseModel, Field
import jwt
from datetime import datetime, timedelta, timezone, date
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph=PasswordHasher()
engine = create_engine("sqlite:///Student.db")
Base = declarative_base()

ACESSS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 
SECRET_KEY = "123SECRET"
ALGORITHM = "HS256"

class StudentCreate(BaseModel):
    roll_no: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=2, max_length=100)
    department: str
    semester: int = Field(ge=1, le=8)

class StudentUpdate(BaseModel):
    roll_no: str = None
    name: str = None
    department: str = None
    semester: int = Field(default=None, ge=1, le=8)

class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: str = "present"

class AttendanceUpdate(BaseModel):
    status: str

class UserAuth(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    role: str = "teacher"

class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_name = Column(String, nullable=False)
    roll_no = Column(String, nullable=False)
    attendance_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

def verify_login(username, password):
    session = Session(engine)
    query = session.query(users).filter(users.username == username).first()
    if query is None:
        session.close()
        return False
    try:
        ph.verify(query.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False
    role = query.role or "teacher"
    session.close()
    access_token = create_token(username=username, role=role, tokentype="access")
    refresh_token = create_token(username=username, role=role, tokentype="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token, "role": role}

def create_token(username: str, role: str = "teacher", tokentype: str = "access"):
    if tokentype == "access":
        payload = {
            "username": username,
            "role": role, 
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACESSS_TOKEN_EXPIRY)
        }
    elif tokentype == "refresh":
        payload = {
            "username": username,
            "role": role,
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRY)
        }

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token, tokentype="access"):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return False

    if payload["tokentype"] == tokentype:
        return {
            "username": payload["username"],
            "role": payload.get("role", "teacher")
        }
    return False