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
VALID_ROLES = ["teacher"]


class UserAuth(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AttendanceCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_no: str = Field(min_length=1)
    attendance_date: date
    status: str = "present"
    
@app.post("/refresh")
def refresh(refresh_token):
    user = functions.verify_token(token=refresh_token, tokentype="refresh")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Token")
    access_token = functions.create_token(username=user["username"], role=user["role"], tokentype="access")
    return {"access_token": access_token}


@app.post("/login")
def login(data: UserAuth):
    tokens = functions.verify_login(username=data.username, password=data.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return tokens

@app.post("/attendance", status_code=201)
def mark_student_attendance(data: AttendanceCreate, token = Header(None)):
    user = functions.verify_token(token=token, tokentype="access")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token.")
    if data.status not in VALID_ATTENDANCE_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid status.")
    result = functions.mark_attendance(
        username=user["username"],
        student_name=data.student_name,
        roll_no=data.roll_no,
        attendance_date=data.attendance_date,
        status=data.status
    )
    if not result:
        raise HTTPException(status_code=404, detail="Teacher not found.")
    return result