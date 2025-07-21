from fastapi import APIRouter, HTTPException
from api.models import Exam, ExamCreate
from api.database import get_connection
from typing import List

router = APIRouter(prefix="/exams", tags=["exams"])

@router.get("/", response_model=List[dict])
def get_exams():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, s.name as subject_name
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        ORDER BY e.created_at DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.get("/{exam_id}", response_model=dict)
def get_exam(exam_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, s.name as subject_name
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        WHERE e.id = %s
    """, (exam_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Exam not found")
    return row

@router.post("/", response_model=Exam)
def create_exam(exam: ExamCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO exams (exam_code, subject_id, title, duration, total_questions, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
        (exam.exam_code, exam.subject_id, exam.title, exam.duration, exam.total_questions, exam.created_by)
    )
    conn.commit()
    exam_id = cursor.lastrowid
    cursor.execute("SELECT * FROM exams WHERE id = %s", (exam_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 

@router.delete("/{exam_id}")
def delete_exam(exam_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Xóa các bản ghi liên quan trong exam_questions trước
        cursor.execute("DELETE FROM exam_questions WHERE exam_id = %s", (exam_id,))
        
        # Xóa các bản ghi liên quan trong student_exams
        cursor.execute("DELETE FROM student_exams WHERE exam_id = %s", (exam_id,))
        
        # Cuối cùng xóa đề thi
        cursor.execute("DELETE FROM exams WHERE id = %s", (exam_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Deleted"}
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error deleting exam: {str(e)}") 