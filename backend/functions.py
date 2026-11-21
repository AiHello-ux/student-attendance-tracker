from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey,Header, create_engine
from sqlalchemy.orm import Session, declarative_base
from pydantic import BaseModel, Field
import jwt
from datetime import datetime , timedelta , timezone
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
    id = Column(Integer , primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(String, default="teacher")

class attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_name = Column(String)
    roll_no = Column(String)
    attendance_date = Column(Date)
    status = Column(String)
    created_at= Column(datetime ,default =datetime.now())




    


