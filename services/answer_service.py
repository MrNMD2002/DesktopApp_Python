from services.api_client import get, post

def get_answers(student_exam_id=None):
    if student_exam_id:
        return get(f"/answers/?student_exam_id={student_exam_id}")
    return get("/answers/")

def get_student_answers(student_exam_id):
    """Lấy danh sách câu trả lời của học sinh cho một bài thi"""
    return get(f"/answers/?student_exam_id={student_exam_id}")

def create_answer(student_exam_id, question_id, selected_answer, is_correct):
    return post("/answers/", json={
        "student_exam_id": student_exam_id,
        "question_id": question_id,
        "selected_answer": selected_answer,
        "is_correct": is_correct
    }) 