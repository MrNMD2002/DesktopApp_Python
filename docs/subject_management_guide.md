# 📚 Hướng dẫn Quản lý Môn học

## 🎯 Tổng quan
Tính năng quản lý môn học cho phép Admin tạo, sửa, xóa các môn học trong hệ thống. Người ra đề (Question Creator) có thể chọn môn học mới để thêm câu hỏi vào ngân hàng đề.

## 👨‍💼 Dành cho Admin

### Truy cập quản lý môn học
1. Đăng nhập với tài khoản Admin
2. Trong cửa sổ Admin, nhấn nút **"📚 Quản lý môn học"**
3. Cửa sổ quản lý môn học sẽ hiển thị

### Thêm môn học mới
1. Nhấn nút **"➕ Thêm môn học"**
2. Điền thông tin:
   - **Tên môn học**: Tên đầy đủ của môn học (VD: "Lập trình Python")
   - **Mã môn học**: Mã viết tắt (VD: "PYTHON")
   - **Mô tả**: Mô tả chi tiết về môn học
3. Nhấn **"✅ Thêm môn học"** để lưu

### Sửa thông tin môn học
1. Chọn môn học trong danh sách
2. Nhấn nút **"✏️ Sửa môn học"**
3. Chỉnh sửa thông tin cần thiết
4. Nhấn **"✅ Cập nhật"** để lưu thay đổi

### Xóa môn học
1. Chọn môn học trong danh sách
2. Nhấn nút **"🗑️ Xóa môn học"**
3. Xác nhận việc xóa
4. ⚠️ **Lưu ý**: Việc xóa môn học sẽ xóa tất cả câu hỏi và đề thi liên quan

### Làm mới danh sách
- Nhấn nút **"🔄 Làm mới"** để cập nhật danh sách môn học

## 📝 Dành cho Question Creator

### Chọn môn học mới
1. Đăng nhập với tài khoản Question Creator
2. Trong dropdown "Môn học", môn học mới sẽ tự động xuất hiện
3. Chọn môn học mới để upload câu hỏi

### Upload câu hỏi cho môn học mới
1. Chọn môn học mới từ dropdown
2. Chọn file .docx chứa câu hỏi
3. Nhấn **"Đọc file"** để import câu hỏi
4. Câu hỏi sẽ được thêm vào ngân hàng đề của môn học mới

## 🔧 Cấu trúc dữ liệu

### Bảng subjects
```sql
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT
);
```

### API Endpoints
- `GET /subjects/` - Lấy danh sách môn học
- `GET /subjects/{id}` - Lấy thông tin môn học cụ thể
- `POST /subjects/` - Tạo môn học mới
- `PUT /subjects/{id}` - Cập nhật môn học
- `DELETE /subjects/{id}` - Xóa môn học

## 📊 Thống kê

### Hiển thị trong Admin
- **ID**: Mã định danh môn học
- **Tên môn học**: Tên đầy đủ
- **Mã môn học**: Mã viết tắt
- **Mô tả**: Mô tả chi tiết
- **Số câu hỏi**: Tổng số câu hỏi trong môn học
- **Ngày tạo**: Thời gian tạo môn học

### Hiển thị trong Question Creator
- **Môn học**: Tên môn học
- **Tổng câu hỏi**: Tổng số câu hỏi
- **Dễ**: Số câu hỏi mức độ dễ
- **Trung bình**: Số câu hỏi mức độ trung bình
- **Khó**: Số câu hỏi mức độ khó

## ⚠️ Lưu ý quan trọng

### Bảo mật
- Chỉ Admin mới có quyền tạo, sửa, xóa môn học
- Question Creator chỉ có quyền xem và chọn môn học

### Ràng buộc dữ liệu
- Mã môn học phải là duy nhất
- Không thể xóa môn học đang có câu hỏi (cascade delete)
- Tên môn học không được để trống

### Hiệu suất
- Danh sách môn học được cache để tăng tốc độ
- Thống kê được tính toán real-time

## 🚀 Tính năng nâng cao

### Tự động tạo mã môn học
- Hệ thống có thể tự động tạo mã từ tên môn học
- Ví dụ: "Lập trình Python" → "PYTHON"

### Import/Export
- Có thể import danh sách môn học từ file Excel
- Export danh sách môn học ra file PDF

### Phân quyền chi tiết
- Admin có thể phân quyền Question Creator cho từng môn học
- Kiểm soát ai được upload câu hỏi cho môn học nào

## 🔍 Troubleshooting

### Lỗi thường gặp
1. **"Mã môn học đã tồn tại"**
   - Giải pháp: Chọn mã môn học khác

2. **"Không thể xóa môn học có câu hỏi"**
   - Giải pháp: Xóa tất cả câu hỏi trước khi xóa môn học

3. **"Môn học mới không xuất hiện trong dropdown"**
   - Giải pháp: Nhấn "Làm mới" hoặc đăng nhập lại

### Liên hệ hỗ trợ
Nếu gặp vấn đề, vui lòng liên hệ Admin hoặc kiểm tra log hệ thống. 