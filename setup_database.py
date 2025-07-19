#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script setup database cho ứng dụng
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    """Setup database"""
    print("=" * 60)
    print("SETUP DATABASE")
    print("=" * 60)
    
    try:
        from database.database_manager import DatabaseManager
        from utils.auth import AuthManager
        
        db = DatabaseManager()
        
        print("✅ Kết nối database thành công")
        
        # Tạo bảng nếu chưa có
        print("\n📋 Tạo bảng...")
        
        # Bảng users
        create_users_table = """
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
        )
        """
        db.execute_query(create_users_table)
        print("✅ Bảng users đã tạo")
        
        # Bảng subjects
        create_subjects_table = """
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            code VARCHAR(20) UNIQUE NOT NULL,
            description TEXT
        )
        """
        db.execute_query(create_subjects_table)
        print("✅ Bảng subjects đã tạo")
        
        # Bảng questions
        create_questions_table = """
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
        )
        """
        db.execute_query(create_questions_table)
        print("✅ Bảng questions đã tạo")
        
        # Bảng question_history
        create_history_table = """
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
        )
        """
        db.execute_query(create_history_table)
        print("✅ Bảng question_history đã tạo")
        
        # Bảng exams
        create_exams_table = """
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
        )
        """
        db.execute_query(create_exams_table)
        print("✅ Bảng exams đã tạo")
        
        # Bảng exam_questions
        create_exam_questions_table = """
        CREATE TABLE IF NOT EXISTS exam_questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            exam_id INT NOT NULL,
            question_id INT NOT NULL,
            question_order INT NOT NULL,
            FOREIGN KEY (exam_id) REFERENCES exams(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        """
        db.execute_query(create_exam_questions_table)
        print("✅ Bảng exam_questions đã tạo")
        
        # Bảng student_exams
        create_student_exams_table = """
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
        )
        """
        db.execute_query(create_student_exams_table)
        print("✅ Bảng student_exams đã tạo")
        
        # Bảng student_answers
        create_student_answers_table = """
        CREATE TABLE IF NOT EXISTS student_answers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_exam_id INT NOT NULL,
            question_id INT NOT NULL,
            selected_answer CHAR(1) NULL,
            is_correct BOOLEAN NULL,
            FOREIGN KEY (student_exam_id) REFERENCES student_exams(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        """
        db.execute_query(create_student_answers_table)
        print("✅ Bảng student_answers đã tạo")
        
        # Thêm dữ liệu mẫu
        print("\n📝 Thêm dữ liệu mẫu...")
        
        # Kiểm tra subjects đã có chưa
        subjects = db.execute_query("SELECT COUNT(*) as count FROM subjects")
        if subjects[0]['count'] == 0:
            insert_subjects = """
            INSERT INTO subjects (name, code, description) VALUES
            ('Toán học', 'MATH', 'Môn học về toán học cơ bản'),
            ('Vật lý', 'PHYSICS', 'Môn học về vật lý'),
            ('Hóa học', 'CHEMISTRY', 'Môn học về hóa học'),
            ('Tiếng Anh', 'ENGLISH', 'Môn học về tiếng Anh')
            """
            db.execute_query(insert_subjects)
            print("✅ Dữ liệu subjects đã thêm")
        
        # Kiểm tra users đã có chưa
        users = db.execute_query("SELECT COUNT(*) as count FROM users")
        if users[0]['count'] == 0:
            # Tạo mật khẩu hash cho "123456"
            auth = AuthManager()
            password_hash = auth.hash_password("123456")
            
            insert_users = """
            INSERT INTO users (username, password_hash, full_name, email, role, is_active) VALUES
            ('admin', %s, 'Administrator', 'admin@example.com', 'admin', TRUE),
            ('creator1', %s, 'Người tạo câu hỏi 1', 'creator1@example.com', 'question_creator', TRUE),
            ('student1', %s, 'Học sinh 1', 'student1@example.com', 'student', TRUE)
            """
            db.execute_query(insert_users, (password_hash, password_hash, password_hash))
            print("✅ Dữ liệu users đã thêm")
        
        print("\n🎉 Setup database hoàn thành!")
        print("📋 Tài khoản mẫu (mật khẩu: 123456):")
        print("   • admin - Quản trị viên")
        print("   • creator1 - Người tạo câu hỏi")
        print("   • student1 - Học sinh")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi setup database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hàm main"""
    print("🚀 SETUP DATABASE CHO ỨNG DỤNG")
    print("=" * 60)
    
    success = setup_database()
    
    if success:
        print("\n✅ Database đã sẵn sàng!")
        print("💡 Bây giờ bạn có thể chạy ứng dụng:")
        print("   python main.py")
    else:
        print("\n❌ Setup database thất bại!")
        print("🔧 Vui lòng kiểm tra:")
        print("   1. MySQL Server đã chạy chưa")
        print("   2. Cấu hình trong config/database_config.py")
        print("   3. Quyền tạo database và bảng")

if __name__ == "__main__":
    main() 