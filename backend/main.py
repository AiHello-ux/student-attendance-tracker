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

VALID_ATTENDANCE_STATUSES = ["present", "absent", "late"]


class UserAuth(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class AttendanceCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_no: str = Field(min_length=1)
    attendance_date: date
    status: str = "present"

class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

@app.post("/register")
def register(data: UserRegister):
    result = functions.register_teacher(
        username=data.username,
        email=data.email,
        password=data.password
    )

    if not result:
        raise HTTPException(status_code=409, detail="Email already exists.")

    return result

@app.get("/get-attendance")
def get_attendance(token=Header(None)):
    user = functions.verify_token(token=token, tokentype="access")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token.")

    result = functions.get_attendance_records(user_id=user["user_id"])

    return result
  
@app.post("/refresh")
def refresh(refresh_token: str):
    user = functions.verify_token(token=refresh_token, tokentype="refresh")
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    access_token = functions.create_token(
        user_id=user["user_id"], 
        email=user["email"], 
        tokentype="access"
    )
    return {"access_token": access_token}

@app.post("/login")
def login(data: UserAuth):
    tokens = functions.verify_login(email=data.email, password=data.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return tokens

@app.post("/attendance")
def mark_student_attendance(data: AttendanceCreate, token = Header(None)):
    user = functions.verify_token(token=token, tokentype="access")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if data.status not in ["present", "absent"]:
        raise HTTPException(status_code=422, detail="Status must be present or absent")
    result = functions.mark_attendance(
        user_id=user["user_id"],
        student_name=data.student_name,
        roll_no=data.roll_no,
        attendance_date=data.attendance_date,
        status=data.status
    )
    if not result:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return result