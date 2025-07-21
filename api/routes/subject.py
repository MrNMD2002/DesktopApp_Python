from fastapi import APIRouter, HTTPException
from api.models import Subject, SubjectCreate
from api.database import get_connection
from typing import List
from database.database_manager import DatabaseManager

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=List[Subject])
def get_subjects():
    """Lấy danh sách môn học với cache"""
    db = DatabaseManager()
    return db.execute_query("SELECT * FROM subjects ORDER BY name", use_cache=True)

@router.get("/{subject_id}", response_model=Subject)
def get_subject(subject_id: int):
    """Lấy thông tin môn học theo ID với cache"""
    db = DatabaseManager()
    result = db.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,), use_cache=True)
    if not result:
        raise HTTPException(status_code=404, detail="Môn học không tồn tại")
    return result[0]

@router.post("/", response_model=Subject)
def create_subject(subject: SubjectCreate):
    """Tạo môn học mới"""
    db = DatabaseManager()
    result = db.execute_query(
        "INSERT INTO subjects (name, code, description) VALUES (%s, %s, %s)",
        (subject.name, subject.code, subject.description)
    )
    subject_id = db.get_last_insert_id()
    return db.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,))[0]

@router.put("/{subject_id}", response_model=Subject)
def update_subject(subject_id: int, subject: SubjectCreate):
    """Cập nhật thông tin môn học"""
    db = DatabaseManager()
    # Kiểm tra môn học có tồn tại không
    existing = db.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Môn học không tồn tại")
    
    db.execute_query(
        "UPDATE subjects SET name = %s, code = %s, description = %s WHERE id = %s",
        (subject.name, subject.code, subject.description, subject_id)
    )
    return db.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,))[0]

@router.delete("/{subject_id}")
def delete_subject(subject_id: int):
    """Xóa môn học"""
    db = DatabaseManager()
    # Kiểm tra môn học có tồn tại không
    existing = db.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Môn học không tồn tại")
    
    # Xóa môn học (cascade sẽ xóa các câu hỏi và đề thi liên quan)
    db.execute_query("DELETE FROM subjects WHERE id = %s", (subject_id,))
    return {"message": "Đã xóa môn học thành công"} 