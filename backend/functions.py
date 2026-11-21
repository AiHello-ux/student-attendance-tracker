from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
from fastapi import Header
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
    session.close()
    
    role = "teacher"
    access_token = create_token(username=username, role=role, tokentype="access")
    refresh_token = create_token(username=username, role=role, tokentype="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token, "role": role}

def create_token(username: str, role: str = "teacher", tokentype: str = "access"):
    if tokentype == "access":
        payload = {
            "username": username,
            "role": "teacher", 
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACESSS_TOKEN_EXPIRY)
        }
    elif tokentype == "refresh":
        payload = {
            "username": username,
            "role": "teacher",
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
            "role": "teacher"
        }
    return False

def mark_attendance(username: str, student_name: str, roll_no: str, attendance_date: date, status: str):
    session = Session(engine)
    teacher = session.query(users).filter(users.username == username).first()
    if not teacher:
        session.close()
        return None
    new_record = attendance(
        user_id=teacher.id,
        student_name=student_name,
        roll_no=roll_no,
        attendance_date=attendance_date,
        status=status
    )
    session.add(new_record)
    session.commit()
    result = {
        "id": new_record.id,
        "user_id": new_record.user_id,
        "student_name": new_record.student_name,
        "roll_no": new_record.roll_no,
        "attendance_date": str(new_record.attendance_date),
        "status": new_record.status,
        "created_at": str(new_record.created_at)
    }
    session.close()
    return result