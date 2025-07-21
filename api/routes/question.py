from fastapi import APIRouter, HTTPException, Query, Body
from api.models import Question, QuestionCreate
from api.database import get_connection
from typing import List, Optional

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=List[Question])
def get_questions(subject_id: Optional[int] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if subject_id:
        cursor.execute("SELECT * FROM questions WHERE subject_id = %s ORDER BY id DESC", (subject_id,))
    else:
        cursor.execute("SELECT * FROM questions ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@router.get("/{question_id}", response_model=Question)
def get_question(question_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Question not found")
    return row

@router.post("/", response_model=Question)
def create_question(question: QuestionCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (question.subject_id, question.question_text, question.option_a, question.option_b, question.option_c, question.option_d, question.correct_answer, question.difficulty_level, question.points, question.created_by)
    )
    conn.commit()
    question_id = cursor.lastrowid
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row 

@router.delete("/{question_id}")
def delete_question(question_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    # Xóa các bản ghi liên quan trong exam_questions trước
    cursor.execute("DELETE FROM exam_questions WHERE question_id = %s", (question_id,))
    cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Deleted"} 

@router.put("/{question_id}")
def update_question(question_id: int, data: dict = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE questions SET
            question_text = %s,
            option_a = %s,
            option_b = %s,
            option_c = %s,
            option_d = %s,
            correct_answer = %s,
            difficulty_level = %s,
            points = %s
        WHERE id = %s
    """, (
        data.get("question_text"),
        data.get("option_a"),
        data.get("option_b"),
        data.get("option_c"),
        data.get("option_d"),
        data.get("correct_answer"),
        data.get("difficulty_level"),
        data.get("points", 1.0),
        question_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Updated"} 