# Hệ thống Quản lý Ngân hàng Đề thi Trắc nghiệm

Ứng dụng desktop Python để quản lý ngân hàng đề thi trắc nghiệm với phân quyền người dùng theo vai trò.

## Tính năng chính

### 1. Người làm đề (Question Creator)
- Upload file .docx chứa câu hỏi theo template có sẵn
- Xem thống kê câu hỏi theo môn học
- Không truy cập trực tiếp vào cơ sở dữ liệu

### 2. Người sinh đề (Exam Generator)
- Tạo đề thi ngẫu nhiên từ ngân hàng câu hỏi
- Chọn môn học, số câu hỏi, thời gian làm bài
- Quản lý danh sách đề thi (xem chi tiết, xóa)
- Đặt mã đề và tên đề thi

### 3. Học sinh (Student)
- Đăng nhập và chọn đề thi để làm bài
- Làm bài thi với giao diện thân thiện
- Hiển thị thời gian còn lại
- Nộp bài và xem điểm ngay lập tức

## Yêu cầu hệ thống

- Python 3.7+
- MySQL Server
- Windows/Linux/macOS

## Cài đặt

### 1. Cài đặt Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Cài đặt và cấu hình MySQL

1. Cài đặt MySQL Server
2. Tạo database và import schema:

```sql
mysql -u root -p < database/schema.sql
```

### 3. Cấu hình kết nối database

Chỉnh sửa file `config/database_config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # Thay đổi mật khẩu MySQL
    'database': 'exam_bank',
    'charset': 'utf8mb4',
    'autocommit': True
}
```

## Chạy ứng dụng

```bash
python main.py
```

## Tài khoản mẫu

Hệ thống đã có sẵn các tài khoản mẫu (mật khẩu: 123456):

- **student1** - Học sinh
- **creator1** - Người làm đề
- **admin** - Người sinh đề

## Định dạng file .docx

Người làm đề cần tạo file .docx theo định dạng sau:

```
Câu 1: Thủ đô của Việt Nam là?
A. Hà Nội
B. TP. Hồ Chí Minh
C. Đà Nẵng
D. Huế
Đáp án: A

Câu 2: 2 + 2 = ?
A. 3
B. 4
C. 5
D. 6
Đáp án: B
```

### Quy tắc định dạng:

1. **Câu hỏi**: Bắt đầu bằng "Câu X:", "X.", "QX:", hoặc "Question X:"
2. **Đáp án**: Bắt đầu bằng A., B., C., D. (hoặc a., b., c., d.)
3. **Đáp án đúng**: Bắt đầu bằng "Đáp án:", "Answer:", "Correct:", hoặc "Đúng:"

## Cấu trúc thư mục

```
DesktopApp_Python/
├── main.py                          # File chính khởi chạy ứng dụng
├── requirements.txt                 # Dependencies Python
├── README.md                       # Hướng dẫn sử dụng
├── config/
│   └── database_config.py          # Cấu hình kết nối database
├── database/
│   ├── database_manager.py         # Module quản lý database
│   └── schema.sql                  # Schema cơ sở dữ liệu
├── utils/
│   ├── auth.py                     # Module xác thực và phân quyền
│   └── docx_reader.py              # Module đọc file .docx
├── gui/
│   ├── login_window.py             # Giao diện đăng nhập
│   ├── student_window.py           # Giao diện học sinh
│   ├── question_creator_window.py  # Giao diện người làm đề
│   └── exam_generator_window.py    # Giao diện người sinh đề
└── templates/
    └── question_template.docx      # Template mẫu cho câu hỏi
```

## Tính năng bảo mật

- Mã hóa mật khẩu bằng bcrypt
- Phân quyền người dùng theo vai trò
- Xác thực đăng nhập
- Kiểm tra quyền truy cập

## Tính năng kỹ thuật

- Giao diện Tkinter hiện đại và thân thiện
- Kết nối MySQL an toàn
- Xử lý lỗi và logging
- Đếm thời gian làm bài tự động
- Tính điểm tự động
- Import câu hỏi từ file .docx

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra MySQL Server đã chạy chưa
- Kiểm tra thông tin kết nối trong `config/database_config.py`
- Đảm bảo database `exam_bank` đã được tạo

### Lỗi import thư viện
- Chạy `pip install -r requirements.txt`
- Kiểm tra Python version (yêu cầu 3.7+)

### Lỗi đọc file .docx
- Đảm bảo file .docx đúng định dạng
- Kiểm tra quyền đọc file
- Cài đặt thư viện python-docx: `pip install python-docx`

## Đóng góp

Để đóng góp vào dự án:

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License - xem file LICENSE để biết thêm chi tiết. 