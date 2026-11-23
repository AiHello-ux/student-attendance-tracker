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

Base.metadata.create_all(engine)

def register_teacher(username: str, email: str, password: str):
    session = Session(engine)

    existing_user = session.query(users).filter(users.email == email).first()

    if existing_user:
        session.close()
        return False

    new_user = users(
        username=username,
        email=email,
        hashed_password=ph.hash(password)
    )

    session.add(new_user)
    session.commit()

    result = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": str(new_user.created_at)
    }

    session.close()
    return result

def get_attendance_records(user_id: int):
    session = Session(engine)

    records = session.query(attendance).filter(attendance.user_id == user_id).all()

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "user_id": record.user_id,
            "student_name": record.student_name,
            "roll_no": record.roll_no,
            "attendance_date": str(record.attendance_date),
            "status": record.status,
            "created_at": str(record.created_at)
        })

    session.close()
    return result

def verify_login(email, password):
    session = Session(engine)
    query = session.query(users).filter(users.email == email).first()
    if query is None:
        session.close()
        return False
    try:
        ph.verify(query.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False    
    user_id = query.id
    session.close()

    access_token = create_token(user_id=user_id, email=email, tokentype="access")
    refresh_token = create_token(user_id=user_id, email=email, tokentype="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token}

def create_token(user_id: int, email: str, tokentype: str = "access"):
    if tokentype == "access":
        payload = {
            "user_id": user_id,
            "email": email,
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACESSS_TOKEN_EXPIRY)
        }
    elif tokentype == "refresh":
        payload = {
            "user_id": user_id,
            "email": email,
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_EXPIRY)
        }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token, tokentype="access"):
    if not token:
        return False
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False
    if payload.get("tokentype") == tokentype:
        return payload
    return False

def mark_attendance(user_id: int, student_name: str, roll_no: str, attendance_date: date, status: str):
    session = Session(engine)
    teacher = session.query(users).filter(users.id == user_id).first()
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