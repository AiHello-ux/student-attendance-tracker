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
VALID_ROLES = ["teacher", "admin"]