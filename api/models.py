from pydantic import BaseModel
from typing import Optional, List
import datetime

class User(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    created_at: datetime.datetime

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str

class Subject(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]

class SubjectCreate(BaseModel):
    name: str
    code: str
    description: Optional[str]

class Question(BaseModel):
    id: int
    subject_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty_level: str
    points: Optional[float] = 1.0
    created_by: int
    created_at: datetime.datetime

class QuestionCreate(BaseModel):
    subject_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty_level: Optional[str] = 'medium'
    points: Optional[float] = 1.0
    created_by: int

class Exam(BaseModel):
    id: int
    exam_code: str
    subject_id: int
    title: str
    duration: int
    total_questions: int
    created_by: int
    created_at: datetime.datetime

class ExamCreate(BaseModel):
    exam_code: str
    subject_id: int
    title: str
    duration: int
    total_questions: int
    created_by: int

class Answer(BaseModel):
    id: int
    student_exam_id: int
    question_id: int
    selected_answer: Optional[str]
    is_correct: Optional[bool]

class AnswerCreate(BaseModel):
    student_exam_id: int
    question_id: int
    selected_answer: Optional[str]
    is_correct: Optional[bool]

class StudentExam(BaseModel):
    id: int
    student_id: int
    exam_id: int
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    score: Optional[float]
    status: str

class StudentExamCreate(BaseModel):
    student_id: int
    exam_id: int
    start_time: Optional[datetime.datetime] = None 