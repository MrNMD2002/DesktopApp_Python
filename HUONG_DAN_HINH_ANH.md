# 📖 HƯỚNG DẪN SỬ DỤNG HÌNH ẢNH TRONG CÂU HỎI

## 🎯 Tổng quan

Hệ thống hỗ trợ nhúng hình ảnh vào câu hỏi thông qua cú pháp `[file:ten_file.jpg]`. Khi import file .docx, hệ thống sẽ tự động trích xuất và lưu hình ảnh.

## 📋 Cú pháp hình ảnh

### ✅ Cú pháp đúng:
```
QN=1: Xem hình và chọn đáp án đúng [file:diagram.jpg]
QN=2: Giải bài toán trong hình [file:math_problem.png]
QN=3: Nhận diện đối tượng trong ảnh [file:object.jpg]
```

### ❌ Cú pháp sai:
```
QN=1: Xem hình và chọn đáp án đúng [diagram.jpg]
QN=2: Giải bài toán trong hình [file diagram.png]
QN=3: Nhận diện đối tượng trong ảnh file:object.jpg
```

## 🖼️ Định dạng hình ảnh hỗ trợ

- **JPG/JPEG**: Hình ảnh thông thường
- **PNG**: Hình ảnh có độ trong suốt
- **GIF**: Hình ảnh động
- **BMP**: Hình ảnh bitmap
- **TIFF**: Hình ảnh chất lượng cao

## 📁 Cấu trúc thư mục

```
project/
├── questions/
│   ├── question_1.docx
│   └── question_2.docx
├── images/
│   ├── diagram.jpg
│   ├── math_problem.png
│   └── object.jpg
└── extracted_images/
    ├── diagram_001.jpg
    ├── math_problem_002.png
    └── object_003.jpg
```

## 🔧 Cách sử dụng

### 1. Chuẩn bị hình ảnh
- Đặt hình ảnh vào thư mục `images/`
- Đặt tên file rõ ràng (ví dụ: `b2b_diagram.jpg`)

### 2. Tạo file .docx
- Sử dụng Word hoặc LibreOffice
- Chèn hình ảnh vào văn bản
- Thêm tham chiếu `[file:ten_file.jpg]` vào câu hỏi

### 3. Import vào hệ thống
- Chọn file .docx trong giao diện
- Hệ thống sẽ tự động:
  - Trích xuất hình ảnh từ file .docx
  - Lưu vào thư mục `extracted_images/`
  - Thay thế tham chiếu bằng đường dẫn thực tế

## 📝 Ví dụ hoàn chỉnh

### File .docx:
```
QUIZ TEMPLATE
Subject: ISC
Number of Quiz: 3
Lecturer: hungpd2
Date: dd-mm-yyyy

QN=1: See the figure and choose the right type of B2B E-Commerce [file:8435.jpg]
a. Sell-side B2B
b. Electronic Exchange
c. Buy-side B2B
d. Supply Chain Improvements and Collaborative Commerce
ANSWER: B
MARK: 0.5
UNIT: Chapter1
MIX CHOICES: Yes

QN=2: What is 15 + 27?
a. 40
b. 42
c. 43
d. 44
ANSWER: B
MARK: 0.5
UNIT: Chapter1
MIX CHOICES: Yes

QN=3: Identify the programming language [file:python_code.png]
a. Java
b. Python
c. C++
d. JavaScript
ANSWER: B
MARK: 0.5
UNIT: Chapter1
MIX CHOICES: Yes
```

### Kết quả sau khi import:
- **Câu hỏi 1**: Có hình ảnh `8435.jpg` được trích xuất
- **Câu hỏi 2**: Không có hình ảnh
- **Câu hỏi 3**: Có hình ảnh `python_code.png` được trích xuất

## 🛠️ Công cụ hỗ trợ

### 1. Tạo file demo:
```bash
python convert_template_to_real_questions.py
# Chọn tùy chọn 3: Tạo file demo với hình ảnh thực tế
```

### 2. Test file:
```bash
python test_file_detailed.py
# Chọn file .docx để test
```

### 3. Debug file:
```bash
python debug_file_content.py
# Phân tích chi tiết nội dung file
```

## ⚠️ Lưu ý quan trọng

1. **Tên file hình ảnh**: Không được chứa ký tự đặc biệt
2. **Đường dẫn**: Sử dụng `/` thay vì `\` trong Windows
3. **Kích thước**: Hình ảnh nên < 5MB để tránh lỗi
4. **Định dạng**: Ưu tiên JPG/PNG để tương thích tốt
5. **Backup**: Luôn backup file gốc trước khi import

## 🔍 Xử lý lỗi

### Lỗi thường gặp:

1. **Không tìm thấy hình ảnh**:
   - Kiểm tra tên file trong tham chiếu
   - Đảm bảo hình ảnh tồn tại trong file .docx

2. **Lỗi trích xuất**:
   - Kiểm tra định dạng file
   - Thử với hình ảnh khác

3. **Lỗi lưu file**:
   - Kiểm tra quyền ghi thư mục
   - Đảm bảo đủ dung lượng ổ đĩa

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy:
1. Chạy công cụ debug để phân tích
2. Kiểm tra log file `app.log`
3. Liên hệ admin để được hỗ trợ

---

**Lưu ý**: Hệ thống tự động xử lý hình ảnh, bạn chỉ cần tuân thủ cú pháp `[file:ten_file.jpg]` trong câu hỏi. 