-- Script cập nhật database để thêm column points
USE exam_bank;

-- Thêm column points vào bảng questions nếu chưa có
ALTER TABLE questions ADD COLUMN IF NOT EXISTS points DECIMAL(3,1) DEFAULT 1.0;

-- Cập nhật tất cả câu hỏi hiện có có điểm mặc định là 1.0
UPDATE questions SET points = 1.0 WHERE points IS NULL;

-- Hiển thị thông tin cập nhật
SELECT 
    'Database updated successfully!' as message,
    COUNT(*) as total_questions,
    SUM(points) as total_points
FROM questions; 