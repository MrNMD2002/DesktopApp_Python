-- Script sửa lỗi database
USE exam_bank;

-- Thêm column points nếu chưa có
ALTER TABLE questions ADD COLUMN IF NOT EXISTS points DECIMAL(3,1) DEFAULT 1.0;

-- Cập nhật tất cả câu hỏi hiện có có điểm mặc định
UPDATE questions SET points = 1.0 WHERE points IS NULL;

-- Kiểm tra kết quả
SELECT 'Database updated successfully!' as status; 