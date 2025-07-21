from services.api_client import get, post, put
from services import answer_service, question_service

def get_student_exams(student_id=None, exam_id=None):
    if student_id:
        return get(f"/student_exams/?student_id={student_id}")
    if exam_id:
        return get(f"/student_exams/?exam_id={exam_id}")
    return get("/student_exams/")

def create_student_exam(student_id, exam_id, start_time=None):
    data = {"student_id": student_id, "exam_id": exam_id}
    if start_time:
        data["start_time"] = start_time
    return post("/student_exams/", json=data)

def update_student_exam_score(student_exam_id, score, status="completed"):
    data = {"score": score, "status": status}
    return put(f"/student_exams/{student_exam_id}", json=data)

def calculate_score(student_exam_id):
    """Tính điểm bài thi dựa trên điểm số từng câu"""
    try:
        # Lấy tất cả câu trả lời của học sinh
        answers = answer_service.get_student_answers(student_exam_id)
        
        if not answers:
            return 0.0
        
        # Tính tổng điểm dựa trên điểm số từng câu
        total_score = 0.0
        for answer in answers:
            if answer.get('is_correct', False):
                # Lấy điểm số của câu hỏi
                question_id = answer.get('question_id')
                if question_id:
                    question = question_service.get_question_by_id(question_id)
                    if question and question.get('points'):
                        total_score += question.get('points', 1.0)
                    else:
                        total_score += 1.0  # Mặc định 1 điểm nếu không có thông tin
                else:
                    total_score += 1.0  # Mặc định 1 điểm
        
        return round(total_score, 2)
    except Exception as e:
        print(f"Lỗi tính điểm: {e}")
        return 0.0