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

### 4. Quản trị viên (Admin)
- **Quản lý người dùng**: Thêm, sửa, xóa, khóa/mở khóa tài khoản
- **Quản lý câu hỏi**: Thêm, sửa, xóa, khôi phục câu hỏi
- **Xem lịch sử**: Xem tất cả lịch sử chỉnh sửa câu hỏi
- **Phân quyền**: Gán vai trò cho người dùng
- **Theo dõi hoạt động**: Xem lịch sử đăng nhập
- **Bảo mật**: Quản lý trạng thái tài khoản

### 5. Giáo viên (Question Creator)
- **Quản lý câu hỏi**: Thêm, sửa, xóa câu hỏi trực tiếp
- **Xem lịch sử**: Xem lịch sử chỉnh sửa câu hỏi của mình
- **Upload file**: Import câu hỏi từ file .docx
- **Thống kê**: Xem thống kê câu hỏi theo môn học

## Tính năng bảo mật và quản lý

### Quản lý mật khẩu
- **Đổi mật khẩu**: Người dùng có thể đổi mật khẩu với xác thực mật khẩu cũ
- **Quên mật khẩu**: Hệ thống tạo token reset mật khẩu có ý nghĩa
- **Token có cấu trúc**: RESET-USERNAME-TIMESTAMP-RANDOM
- **Hạn sử dụng**: Token có hiệu lực trong 1 giờ
- **Bảo mật**: Mã hóa mật khẩu bằng bcrypt

### Quản lý tài khoản
- **Phân quyền**: 4 vai trò chính (admin, question_creator, exam_generator, student)
- **Khóa/mở khóa**: Quản trị viên có thể khóa tài khoản người dùng
- **Theo dõi hoạt động**: Lưu lịch sử đăng nhập và thay đổi
- **Soft delete**: Xóa mềm với khả năng khôi phục

## Cài đặt

1. **Cài đặt Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Cấu hình database:**
- Tạo database MySQL tên `exam_bank`
- Chỉnh sửa thông tin kết nối trong `config/database_config.py`
- Chạy script setup database: `python setup_database.py`

3. **Chạy ứng dụng:**
```bash
python main.py
```

## Setup Database

Để setup database tự động:

```bash
python setup_database.py
```

Script này sẽ:
- Tạo tất cả các bảng cần thiết
- Thêm dữ liệu mẫu (môn học, tài khoản)
- Tạo tài khoản mẫu với mật khẩu: `123456`

## Demo chức năng Token có ý nghĩa

Để xem demo chức năng token reset mật khẩu:

```bash
python test_token_demo.py
```

Demo sẽ hiển thị:
- Cấu trúc token: RESET-USERNAME-TIMESTAMP-RANDOM
- Tạo token cho các user khác nhau
- Giải mã thông tin từ token
- Kiểm tra tính hợp lệ của token

## Demo chức năng Đọc File Word

Để xem demo chức năng đọc file Word với định dạng mới:

```bash
python test_docx_reader.py
```

Demo sẽ hiển thị:
- Các hàm parse riêng lẻ
- Hướng dẫn định dạng template
- Tạo và đọc file Word test
- Hỗ trợ định dạng MARK, UNIT, MIX CHOICES

## Demo chức năng Hỗ trợ Hình ảnh

Để xem demo chức năng hỗ trợ hình ảnh trong file .docx:

```bash
python test_image_support.py
```

Demo sẽ hiển thị:
- Trích xuất hình ảnh từ file .docx
- Xử lý tham chiếu [file:filename]
- Lưu hình ảnh vào thư mục extracted_images/
- Test xử lý hoàn chỉnh file có hình ảnh

## 🖼️ Hỗ trợ hình ảnh trong câu hỏi

Hệ thống hỗ trợ nhúng hình ảnh vào câu hỏi thông qua cú pháp `[file:ten_file.jpg]`.

### Cú pháp hình ảnh:
```
QN=1: Xem hình và chọn đáp án đúng [file:diagram.jpg]
QN=2: Giải bài toán trong hình [file:math_problem.png]
QN=3: Nhận diện đối tượng trong ảnh [file:object.jpg]
```

### Định dạng hỗ trợ:
- **JPG/JPEG**: Hình ảnh thông thường
- **PNG**: Hình ảnh có độ trong suốt
- **GIF**: Hình ảnh động
- **BMP**: Hình ảnh bitmap
- **TIFF**: Hình ảnh chất lượng cao

### Cách sử dụng:
1. **Chuẩn bị hình ảnh**: Đặt hình ảnh vào thư mục `images/`
2. **Tạo file .docx**: Chèn hình ảnh và thêm tham chiếu `[file:ten_file.jpg]`
3. **Import vào hệ thống**: Chọn file .docx trong giao diện
4. **Tự động xử lý**: Hình ảnh được trích xuất và lưu vào `extracted_images/`

### Công cụ hỗ trợ hình ảnh:

#### 1. Tạo file demo với hình ảnh:
```bash
python convert_template_to_real_questions.py
# Chọn tùy chọn 3: Tạo file demo với hình ảnh thực tế
```

#### 2. Test chức năng hình ảnh:
```bash
python test_image_support.py
```

#### 3. Debug file có hình ảnh:
```bash
python debug_file_content.py
```

### Ví dụ hoàn chỉnh:
```
QN=1: See the figure and choose the right type of B2B E-Commerce [file:8435.jpg]
a. Sell-side B2B
b. Electronic Exchange
c. Buy-side B2B
d. Supply Chain Improvements and Collaborative Commerce
ANSWER: B
MARK: 0.5
UNIT: Chapter1
MIX CHOICES: Yes
```

### Lưu ý quan trọng:
- Tên file hình ảnh không được chứa ký tự đặc biệt
- Kích thước hình ảnh nên < 5MB
- Ưu tiên định dạng JPG/PNG để tương thích tốt
- Luôn backup file gốc trước khi import

**Xem chi tiết**: [HUONG_DAN_HINH_ANH.md](HUONG_DAN_HINH_ANH.md)

## Tài khoản mẫu

Hệ thống đã có sẵn các tài khoản mẫu (mật khẩu: 123456):

- **student1** - Học sinh
- **creator1** - Người làm đề
- **admin** - Quản trị viên (có quyền quản lý user)

## Định dạng file .docx

Người làm đề cần tạo file .docx theo định dạng sau:

### Định dạng cơ bản:
```
QN=1: See the figure and choose the right type of B2B E-Commerce [file:8435.jpg]
a. Sell-side B2B
b. Electronic Exchange
c. Buy-side B2B
d. Supply Chain Improvements and Collaborative Commerce
ANSWER: B
MARK: 0.5
UNIT: Chapter1
MIX CHOICES: Yes
```

### Định dạng tiếng Việt:
```
Câu 3: Thủ đô của Việt Nam là?
A. Hà Nội
B. TP. Hồ Chí Minh
C. Đà Nẵng
D. Huế
Đáp án: A
Điểm: 1.0
Đơn vị: Địa lý
```

### Quy tắc định dạng:

1. **Câu hỏi**: Bắt đầu bằng "QN=X:", "Câu X:", "X.", "QX:", hoặc "Question X:"
2. **Hình ảnh**: 
   - Chèn hình ảnh trực tiếp vào file .docx
   - Thêm tham chiếu [file:filename] trong text câu hỏi
   - Hình ảnh sẽ được tự động trích xuất và lưu
3. **Đáp án**: Bắt đầu bằng A., B., C., D. (hoặc a., b., c., d.)
4. **Đáp án đúng**: Bắt đầu bằng "ANSWER:", "Đáp án:", "Answer:", "Correct:", hoặc "Đúng:"
5. **Thông tin bổ sung (tùy chọn)**:
   - MARK: Điểm số (ví dụ: 0.5, 1.0)
   - UNIT: Đơn vị bài học (ví dụ: Chapter1, Địa lý)
   - MIX CHOICES: Có trộn đáp án không (Yes/No)

### Hỗ trợ định dạng:
- ✅ QN=1: Câu hỏi
- ✅ Câu 1: Câu hỏi
- ✅ 1. Câu hỏi
- ✅ Q1: Câu hỏi
- ✅ a. Đáp án A
- ✅ A. Đáp án A
- ✅ a) Đáp án A
- ✅ ANSWER: A
- ✅ Đáp án: A
- ✅ MARK: 0.5
- ✅ UNIT: Chapter1
- ✅ MIX CHOICES: Yes
- ✅ Hình ảnh: JPG, PNG, GIF, BMP
- ✅ Tham chiếu: [file:filename]

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
│   ├── docx_reader.py              # Module đọc file .docx
│   └── question_manager.py         # Module quản lý câu hỏi và lịch sử
├── gui/
│   ├── login_window.py             # Giao diện đăng nhập
│   ├── student_window.py           # Giao diện học sinh
│   ├── question_creator_window.py  # Giao diện người làm đề
│   ├── exam_generator_window.py    # Giao diện người sinh đề
│   ├── user_management_window.py   # Giao diện quản lý user (admin)
│   ├── password_window.py          # Giao diện đổi/quên mật khẩu
│   └── question_management_window.py # Giao diện quản lý câu hỏi
└── templates/
    └── question_template.docx      # Template mẫu cho câu hỏi
```

## Tính năng bảo mật

- Mã hóa mật khẩu bằng bcrypt
- Phân quyền người dùng theo vai trò
- Xác thực đăng nhập
- Kiểm tra quyền truy cập
- Token reset mật khẩu an toàn
- Khóa/mở khóa tài khoản
- Theo dõi hoạt động đăng nhập

## Tính năng kỹ thuật

- Giao diện Tkinter hiện đại và thân thiện
- Kết nối MySQL an toàn
- Xử lý lỗi và logging
- Đếm thời gian làm bài tự động
- Tính điểm tự động
- Import câu hỏi từ file .docx
- Quản lý câu hỏi trực tiếp trên giao diện
- Lịch sử chỉnh sửa với JSON backup
- Soft delete với khả năng khôi phục
- Thống kê chi tiết theo nhiều tiêu chí

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra MySQL Server đã chạy chưa
- Kiểm tra thông tin kết nối trong `config/database_config.py`
- Đảm bảo database `exam_bank` đã được tạo
- Chạy script setup: `python setup_database.py`

### Lỗi bảng không tồn tại
- Chạy script setup database: `python setup_database.py`
- Kiểm tra quyền tạo bảng trong MySQL
- Đảm bảo database `exam_bank` đã được tạo trước

### Lỗi import thư viện
- Chạy `pip install -r requirements.txt`
- Kiểm tra Python version (yêu cầu 3.7+)

### Lỗi đọc file Word
- Đảm bảo file .docx đúng định dạng theo hướng dẫn
- Kiểm tra quyền đọc file
- Cài đặt thư viện python-docx: `pip install python-docx`
- Kiểm tra định dạng câu hỏi, đáp án, và thông tin bổ sung
- Chạy demo để test: `python test_docx_reader.py`
- Chạy test khắc phục lỗi: `python test_file_reading.py`
- Sử dụng nút "Test File" trong giao diện để kiểm tra file trước khi import
- Sử dụng nút "Tạo File Mẫu" để tạo file test
- Kiểm tra log file `app.log` để xem lỗi chi tiết

## Đóng góp

Nếu bạn muốn đóng góp cho dự án, vui lòng:

1. Fork repository
2. Tạo branch mới cho tính năng
3. Commit thay đổi
4. Push lên branch
5. Tạo Pull Request

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## Liên hệ

Nếu có câu hỏi hoặc gặp vấn đề, vui lòng tạo issue trên GitHub hoặc liên hệ qua email. 