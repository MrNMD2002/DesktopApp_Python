#!/usr/bin/env python3
"""
Script để xóa và tạo lại database exam_bank
"""
import mysql.connector
from config.database_config import DB_CONFIG
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Xóa và tạo lại database"""
    try:
        # Kết nối MySQL không chỉ định database
        config_without_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
        conn = mysql.connector.connect(**config_without_db)
        cursor = conn.cursor()
        
        logger.info("Đang xóa database cũ...")
        cursor.execute("DROP DATABASE IF EXISTS exam_bank")
        
        logger.info("Đang tạo database mới...")
        cursor.execute("CREATE DATABASE exam_bank")
        
        cursor.close()
        conn.close()
        
        # Kết nối vào database mới
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        logger.info("Đang tạo các bảng...")
        
        # Tạo bảng users
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role ENUM('question_creator', 'exam_generator', 'student', 'admin') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tạo bảng subjects
        cursor.execute("""
            CREATE TABLE subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                description TEXT
            )
        """)
        
        # Tạo bảng questions
        cursor.execute("""
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
                created_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Tạo bảng exams
        cursor.execute("""
            CREATE TABLE exams (
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
            )
        """)
        
        # Tạo bảng exam_questions
        cursor.execute("""
            CREATE TABLE exam_questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                exam_id INT NOT NULL,
                question_id INT NOT NULL,
                question_order INT NOT NULL,
                FOREIGN KEY (exam_id) REFERENCES exams(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        """)
        
        # Tạo bảng student_exams
        cursor.execute("""
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
            )
        """)
        
        # Tạo bảng student_answers
        cursor.execute("""
            CREATE TABLE student_answers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_exam_id INT NOT NULL,
                question_id INT NOT NULL,
                selected_answer CHAR(1) NULL,
                is_correct BOOLEAN NULL,
                FOREIGN KEY (student_exam_id) REFERENCES student_exams(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        """)
        
        logger.info("Đang thêm dữ liệu mẫu...")
        
        # Thêm subjects
        cursor.execute("""
            INSERT INTO subjects (name, code, description) VALUES
            ('Toán học', 'MATH', 'Môn học về toán học cơ bản'),
            ('Vật lý', 'PHYSICS', 'Môn học về vật lý'),
            ('Hóa học', 'CHEMISTRY', 'Môn học về hóa học'),
            ('Tiếng Anh', 'ENGLISH', 'Môn học về tiếng Anh')
        """)
        
        # Thêm users (password: 123456)
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, role) VALUES
            ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Administrator', 'admin'),
            ('creator1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Người tạo câu hỏi 1', 'question_creator'),
            ('student1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Học sinh 1', 'student')
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ Database đã được tạo lại thành công!")
        logger.info("📋 Tài khoản mẫu (mật khẩu: 123456):")
        logger.info("   - admin (Administrator)")
        logger.info("   - creator1 (Người tạo câu hỏi)")
        logger.info("   - student1 (Học sinh)")
        
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Đang reset database...")
    reset_database()
    print("✅ Hoàn thành!") 