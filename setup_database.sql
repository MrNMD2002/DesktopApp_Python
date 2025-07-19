-- Setup Database cho Hệ thống Quản lý Đề thi
-- Chạy file này trong MySQL để tạo database và bảng

-- Tạo database
CREATE DATABASE IF NOT EXISTS exam_bank;
USE exam_bank;

-- Bảng người dùng
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role ENUM('question_creator', 'exam_generator', 'student', 'admin') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    reset_token VARCHAR(255) NULL,
    reset_token_expires TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng môn học
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT
);

-- Bảng câu hỏi
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    difficulty_level ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    created_by INT NOT NULL,
    updated_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Bảng lịch sử chỉnh sửa câu hỏi
CREATE TABLE IF NOT EXISTS question_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    action ENUM('created', 'updated', 'deleted', 'restored') NOT NULL,
    old_data JSON NULL,
    new_data JSON NULL,
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (changed_by) REFERENCES users(id)
);

-- Bảng đề thi
CREATE TABLE IF NOT EXISTS exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_code VARCHAR(20) UNIQUE NOT NULL,
    subject_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    duration INT NOT NULL,
    total_questions INT NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng chi tiết đề thi (câu hỏi trong đề)
CREATE TABLE IF NOT EXISTS exam_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT NOT NULL,
    question_id INT NOT NULL,
    question_order INT NOT NULL,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Bảng bài thi của học sinh
CREATE TABLE IF NOT EXISTS student_exams (
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
CREATE TABLE IF NOT EXISTS student_answers (
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
('Tiếng Anh', 'ENGLISH', 'Môn học về tiếng Anh')
ON DUPLICATE KEY UPDATE name=name;

-- Thêm tài khoản mẫu (password: 123456)
-- Hash được tạo bằng bcrypt cho mật khẩu "123456"
INSERT INTO users (username, password_hash, full_name, email, role, is_active) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Administrator', 'admin@example.com', 'admin', TRUE),
('creator1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Người tạo câu hỏi 1', 'creator1@example.com', 'question_creator', TRUE),
('student1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Học sinh 1', 'student1@example.com', 'student', TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Hiển thị thông tin
SELECT 'Database setup completed!' as status;
SELECT COUNT(*) as user_count FROM users;
SELECT COUNT(*) as subject_count FROM subjects; 