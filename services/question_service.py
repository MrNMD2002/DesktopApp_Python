from services.api_client import get, post, delete, put
import random

def get_questions(subject_id=None):
    """Lấy danh sách câu hỏi với cache"""
    if subject_id:
        return get(f"/questions/?subject_id={subject_id}", use_cache=True)
    return get("/questions/", use_cache=True)

def get_question_by_id(question_id):
    """Lấy thông tin câu hỏi theo ID với cache"""
    return get(f"/questions/{question_id}", use_cache=True)

def get_question(question_id):
    return get(f"/questions/{question_id}")

def create_question(subject_id, question_text, option_a, option_b, option_c, option_d, correct_answer, created_by, difficulty_level='medium', points=1.0):
    return post("/questions/", json={
        "subject_id": subject_id,
        "question_text": question_text,
        "option_a": option_a,
        "option_b": option_b,
        "option_c": option_c,
        "option_d": option_d,
        "correct_answer": correct_answer,
        "difficulty_level": difficulty_level,
        "points": points,
        "created_by": created_by
    })

def update_question(question_id, data):
    return put(f"/questions/{question_id}", json=data)

def get_available_questions_count(subject_id):
    questions = get_questions(subject_id)
    return {"count": len(questions)}

def get_random_questions(subject_id, count):
    questions = get_questions(subject_id)
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

def add_questions_to_exam(exam_questions):
    """
    exam_questions: List of tuple (exam_id, question_id, question_order)
    """
    for exam_id, question_id, question_order in exam_questions:
        try:
            # Nếu question_id là dict, lấy trường 'id'
            if isinstance(question_id, dict):
                question_id = question_id.get('id')
            post("/exam_questions/", json={
                "exam_id": int(exam_id),
                "question_id": int(question_id),
                "question_order": int(question_order)
            })
        except Exception as e:
            print(f"Lỗi khi thêm câu hỏi vào đề: exam_id={exam_id}, question_id={question_id}, question_order={question_order}, error={e}")

def get_exam_questions(exam_id):
    return get(f"/exam_questions/with_questions/?exam_id={exam_id}")

def delete_questions_from_exam(exam_id):
    # Tạm thời gọi API xóa từng câu hỏi (nên bổ sung API backend)
    delete(f"/exam_questions/{exam_id}")

def delete_question(question_id):
    return delete(f"/questions/{question_id}") 