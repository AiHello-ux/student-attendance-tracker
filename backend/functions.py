from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from pydantic import BaseModel, Field
import functions

app = FastAPI(
    title="Student Attendance Management System",
    description="Student Attendance Tracker"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

VALID_ATTENDANCE_STATUSES = ["present", "absent"]
VALID_ROLES = ["teacher", "admin"]

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

