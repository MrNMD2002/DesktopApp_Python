-- Tạo database
CREATE DATABASE IF NOT EXISTS exam_bank;
USE exam_bank;

-- Bảng người dùng
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('question_creator', 'exam_generator', 'student', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng môn học
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT
);

-- Bảng câu hỏi
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    difficulty_level ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    points DECIMAL(3,1) DEFAULT 1.0,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng đề thi
CREATE TABLE exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_code VARCHAR(20) UNIQUE NOT NULL,
    subject_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    duration INT NOT NULL, -- thời gian làm bài (phút)
    total_questions INT NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng chi tiết đề thi (câu hỏi trong đề)
CREATE TABLE exam_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT NOT NULL,
    question_id INT NOT NULL,
    question_order INT NOT NULL,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Bảng bài thi của học sinh
CREATE TABLE student_exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    score DECIMAL(5,2) NULL,
    status ENUM('in_progress', 'completed', 'timeout') DEFAULT 'in_progress',
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id)
);

-- Bảng câu trả lời của học sinh
CREATE TABLE student_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_exam_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_answer CHAR(1) NULL,
    is_correct BOOLEAN NULL,
    FOREIGN KEY (student_exam_id) REFERENCES student_exams(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Thêm dữ liệu mẫu
INSERT INTO subjects (name, code, description) VALUES
('Toán học', 'MATH', 'Môn học về toán học cơ bản'),
('Vật lý', 'PHYSICS', 'Môn học về vật lý'),
('Hóa học', 'CHEMISTRY', 'Môn học về hóa học'),
('Tiếng Anh', 'ENGLISH', 'Môn học về tiếng Anh');

-- Thêm tài khoản mẫu (password: 123456)
INSERT INTO users (username, password_hash, full_name, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Administrator', 'admin'),
('creator1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Người tạo câu hỏi 1', 'question_creator'),
('student1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Học sinh 1', 'student');

UPDATE users SET password_hash='$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO' WHERE username='admin';

SELECT DATABASE(); 