-- Script sửa database cũ (giữ lại dữ liệu)
-- Chạy từng lệnh một để tránh mất dữ liệu

USE exam_bank;

-- Bước 1: Xóa bảng roles nếu có
DROP TABLE IF EXISTS roles;

-- Bước 2: Kiểm tra cấu trúc bảng users hiện tại
-- DESCRIBE users;

-- Bước 3: Thêm cột role nếu chưa có
ALTER TABLE users ADD COLUMN IF NOT EXISTS role ENUM('question_creator', 'exam_generator', 'student', 'admin') NOT NULL DEFAULT 'student';

-- Bước 4: Nếu có cột role_id, cập nhật role và xóa role_id
-- (Bỏ comment nếu có cột role_id)
-- UPDATE users SET role = 'admin' WHERE role_id = 1;
-- UPDATE users SET role = 'question_creator' WHERE role_id = 2;
-- UPDATE users SET role = 'exam_generator' WHERE role_id = 3;
-- UPDATE users SET role = 'student' WHERE role_id = 4;
-- ALTER TABLE users DROP COLUMN IF EXISTS role_id;

-- Bước 5: Đổi tên cột password thành password_hash nếu cần
-- (Bỏ comment nếu cột tên là 'password')
-- ALTER TABLE users CHANGE COLUMN password password_hash VARCHAR(255) NOT NULL;

-- Bước 6: Thêm các cột cần thiết
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255) NULL,
ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Bước 7: Cập nhật role cho user hiện có
UPDATE users SET role = 'admin' WHERE username = 'admin';
UPDATE users SET role = 'question_creator' WHERE username LIKE '%creator%';
UPDATE users SET role = 'exam_generator' WHERE username LIKE '%generator%';
UPDATE users SET role = 'student' WHERE username LIKE '%student%' OR role = 'student';
UPDATE users SET role = 'student' WHERE role IS NULL OR role = '';

-- Bước 8: Thêm tài khoản mẫu nếu chưa có
INSERT IGNORE INTO users (username, password_hash, full_name, email, role, is_active) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Administrator', 'admin@example.com', 'admin', TRUE),
('creator1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Người tạo câu hỏi 1', 'creator1@example.com', 'question_creator', TRUE),
('student1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Học sinh 1', 'student1@example.com', 'student', TRUE);

-- Bước 9: Kiểm tra kết quả
SELECT 'Database fixed successfully!' as status;
SELECT username, full_name, role, is_active FROM users; 