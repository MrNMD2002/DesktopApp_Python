from docx import Document
import re
import logging
from database.database_manager import DatabaseManager
import os


class DocxReader:
    def __init__(self):
        """
        Khởi tạo DocxReader và tạo thư mục 'pictures' nếu chưa tồn tại.
        """
        self.db = DatabaseManager()
        self.pictures_dir = "pictures"
        if not os.path.exists(self.pictures_dir):
            os.makedirs(self.pictures_dir)
            logging.info(f"Đã tạo thư mục lưu trữ hình ảnh: {self.pictures_dir}")

    def extract_images_from_docx(self, doc):
        """
        Trích xuất tất cả các hình ảnh từ một đối tượng tài liệu docx.
        """
        try:
            images = []
            # Duyệt qua các mối quan hệ của tài liệu để tìm hình ảnh
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    image_data = rel.target_part.blob
                    image_name = os.path.basename(rel.target_ref)
                    images.append({'name': image_name, 'data': image_data})
            logging.info(f"Trích xuất được {len(images)} hình ảnh từ file.")
            return images
        except Exception as e:
            logging.error(f"Lỗi trong quá trình trích xuất hình ảnh: {e}")
            return []

    def read_docx_file(self, file_path, subject_id, creator_id):
        """
        Đọc file .docx và trích xuất câu hỏi.
        Hàm này thực hiện theo quy trình 2 bước:
        1. Phân tích toàn bộ file để lấy danh sách câu hỏi.
        2. Kiểm tra sự khớp lệ giữa số lượng tag hình ảnh và số lượng hình ảnh thực tế.
        3. Nếu hợp lệ, tiến hành lưu vào cơ sở dữ liệu.
        """
        try:
            if not os.path.exists(file_path) or not file_path.lower().endswith('.docx'):
                logging.error(f"File không hợp lệ: {file_path}")
                return False, "File không tồn tại hoặc không phải định dạng .docx"

            logging.info(f"Bắt đầu đọc file theo định dạng BẢNG: {file_path}")
            doc = Document(file_path)

            all_images_in_doc = self.extract_images_from_docx(doc)
            parsed_questions = []

            # --- BƯỚC 1: PHÂN TÍCH FILE VÀ TẠO DANH SÁCH CÂU HỎI ---
            for i, table in enumerate(doc.tables):
                current_question = self._create_empty_question()
                is_valid_question_block = False

                for row in table.rows:
                    if len(row.cells) < 2:
                        continue
                    label = row.cells[0].text.strip()
                    value = row.cells[1].text.strip()
                    if not label:
                        continue

                    if self._is_question_start(label):
                        is_valid_question_block = True
                        current_question['question_number'] = self._extract_question_number(label)
                        if '[file:' in value:
                            current_question['has_image'] = True
                            current_question['question_text'] = re.sub(r'\[file:[^\]]+\]', '', value).strip()
                        else:
                            current_question['question_text'] = value
                    elif is_valid_question_block:
                        if self._is_option(label):
                            current_question['options'][label.replace('.', '').strip().upper()] = value
                        elif self._is_correct_answer(label):
                            current_question['correct_answer'] = value.strip().upper()
                        elif self._is_mark_info(label):
                            current_question['mark'] = self._extract_mark(value)
                        elif self._is_unit_info(label):
                            current_question['unit'] = value
                        elif self._is_mix_choices_info(label):
                            current_question['mix_choices'] = self._extract_mix_choices(value)

                if is_valid_question_block and self._is_valid_question(current_question):
                    parsed_questions.append(current_question)
                elif is_valid_question_block:
                    logging.warning(
                        f"Bỏ qua câu hỏi không hợp lệ từ bảng {i + 1} (QN={current_question.get('question_number')})")

            if not parsed_questions:
                return False, "Không tìm thấy câu hỏi hợp lệ nào trong các bảng của file. Vui lòng kiểm tra định dạng."

            # --- BƯỚC 2: KIỂM TRA SỰ KHỚP LỆ CỦA HÌNH ẢNH ---
            num_image_tags = sum(1 for q in parsed_questions if q.get('has_image'))
            num_extracted_images = len(all_images_in_doc)

            if num_image_tags != num_extracted_images:
                error_msg = (
                    f"Phát hiện không khớp: Tìm thấy {num_image_tags} câu hỏi có tag hình ảnh "
                    f"nhưng chỉ trích xuất được {num_extracted_images} hình ảnh từ file.\n\n"
                    "Nguyên nhân có thể là do bạn đã sao chép và dán cùng một hình ảnh nhiều lần. "
                    "Để khắc phục, vui lòng xóa các hình ảnh và chèn lại từng hình ảnh một cách riêng biệt.\n\n"
                    "Quá trình nhập đã bị hủy để đảm bảo tính toàn vẹn dữ liệu."
                )
                logging.error(error_msg)
                return False, error_msg

            # --- BƯỚC 3: LƯU CÂU HỎI VÀO CSDL ---
            image_iterator = iter(all_images_in_doc)
            saved_count = 0
            for question in parsed_questions:
                image_to_save = None
                if question.get('has_image'):
                    try:
                        image_to_save = next(image_iterator)
                    except StopIteration:
                        # Trường hợp này không nên xảy ra do đã kiểm tra ở trên, nhưng vẫn là một biện pháp an toàn
                        logging.error(
                            f"Lỗi logic: Không còn hình ảnh trong iterator cho câu hỏi QN={question.get('question_number')}")
                        continue

                if self._save_question_to_db(question, subject_id, creator_id, image_to_save):
                    saved_count += 1

            success_message = f"Đã đọc thành công {len(parsed_questions)} câu hỏi, lưu {saved_count} câu hỏi vào DB."
            return True, success_message

        except Exception as e:
            logging.error(f"Lỗi nghiêm trọng khi đọc file .docx: {e}", exc_info=True)
            return False, f"Lỗi đọc file: {str(e)}"

    def _save_question_to_db(self, question, subject_id, creator_id, image_data=None):
        """
        Lưu câu hỏi vào cơ sở dữ liệu.
        Nếu có hình ảnh, lưu file ảnh vào thư mục 'pictures' với tên là ID của câu hỏi.
        Không lưu đường dẫn ảnh vào DB.
        """
        try:
            # --- Bước 1: INSERT câu hỏi vào CSDL để lấy ID ---
            additional_info = []
            if question.get('unit'):
                additional_info.append(f"Unit: {question['unit']}")
            if question.get('mark') and question['mark'] != 1.0:
                additional_info.append(f"Mark: {question['mark']}")
            if question.get('mix_choices'):
                additional_info.append("Mix Choices: Yes")

            full_question_text = question['question_text']
            if additional_info:
                full_question_text += f"\n[{' | '.join(additional_info)}]"

            query_insert = """
                           INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d,
                                                  correct_answer, difficulty_level, created_by)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                           """
            params_insert = (
                subject_id, full_question_text,
                question['options'].get('A', ''), question['options'].get('B', ''),
                question['options'].get('C', ''), question['options'].get('D', ''),
                question['correct_answer'], question['difficulty'], creator_id
            )

            # SỬA LỖI: Thay thế phương thức không tồn tại 'execute_insert_and_get_id'
            # bằng một quy trình 2 bước.

            # Bước 1.1: Thực thi câu lệnh INSERT. Giả định bạn có phương thức `execute_query`.
            self.db.execute_query(query_insert, params_insert)

            # Bước 1.2: Lấy ID của bản ghi vừa được chèn.
            # YÊU CẦU QUAN TRỌNG: Lớp 'DatabaseManager' của bạn PHẢI có một phương thức
            # để lấy ID của bản ghi vừa được chèn. Ví dụ: get_last_insert_id().
            # Phương thức này sẽ chứa logic phù hợp với CSDL của bạn (ví dụ: return self.cursor.lastrowid).
            new_question_id = self.db.get_last_insert_id()

            if not new_question_id:
                logging.error(
                    f"Không thể lấy ID cho câu hỏi vừa tạo trong DB (QN={question.get('question_number')}). Đảm bảo get_last_insert_id() được triển khai trong DatabaseManager.")
                return False

            # --- Bước 2: Lưu hình ảnh vào thư mục nếu có ---
            if image_data:
                try:
                    # Xác định đuôi file, mặc định là .png
                    image_extension = os.path.splitext(image_data['name'])[1] if os.path.splitext(image_data['name'])[
                        1] else '.png'
                    image_filename = f"{new_question_id}{image_extension}"
                    image_path = os.path.join(self.pictures_dir, image_filename)

                    # Lưu file hình ảnh
                    with open(image_path, 'wb') as f:
                        f.write(image_data['data'])

                    logging.info(f"Đã lưu hình ảnh '{image_path}' cho câu hỏi ID {new_question_id}.")

                except Exception as img_e:
                    logging.error(f"Lỗi khi lưu hình ảnh cho câu hỏi ID {new_question_id}: {img_e}")
                    # Việc lưu câu hỏi đã thành công, chỉ có lưu ảnh bị lỗi, nên không trả về False

            return True

        except Exception as e:
            # Thêm kiểm tra AttributeError để đưa ra thông báo lỗi rõ ràng hơn
            if isinstance(e, AttributeError) and 'get_last_insert_id' in str(e):
                logging.error(
                    f"LỖI CẤU HÌNH: Vui lòng triển khai phương thức 'get_last_insert_id' trong lớp DatabaseManager của bạn.")
            else:
                logging.error(f"Lỗi lưu câu hỏi (QN={question.get('question_number')}) vào DB: {e}")
            return False

    def _create_empty_question(self):
        """Tạo một cấu trúc câu hỏi trống."""
        return {
            'question_text': '',
            'options': {},
            'correct_answer': None,
            'difficulty': 'medium',
            'mark': 1.0,
            'unit': '',
            'mix_choices': False,
            'has_image': False,
            'question_number': None,
        }

    def _is_valid_question(self, question):
        """Kiểm tra câu hỏi có hợp lệ không"""
        if not question:
            return False
        has_text = bool(question.get('question_text'))
        has_enough_options = len(question.get('options', {})) >= 4
        has_correct_answer_format = question.get('correct_answer') in ['A', 'B', 'C', 'D']
        correct_answer_in_options = question.get('correct_answer') in question.get('options', {})
        return has_text and has_enough_options and has_correct_answer_format and correct_answer_in_options

    # --- Các hàm helper để nhận dạng các dòng trong bảng ---
    def _is_question_start(self, text):
        return re.match(r'^QN\s*=\s*\d+', text, re.IGNORECASE)

    def _extract_question_number(self, text):
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else None

    def _is_option(self, text):
        return re.match(r'^[a-f]\.', text, re.IGNORECASE)

    def _is_correct_answer(self, text):
        return text.strip().upper().startswith('ANSWER')

    def _is_mark_info(self, text):
        return text.strip().upper().startswith('MARK')

    def _is_unit_info(self, text):
        return text.strip().upper().startswith('UNIT')

    def _is_mix_choices_info(self, text):
        return text.strip().upper().startswith('MIX CHOICES')

    def _extract_mark(self, value_text):
        match = re.search(r'(\d+\.?\d*)', value_text)
        try:
            return float(match.group(1)) if match else 1.0
        except (ValueError, AttributeError):
            return 1.0

    def _extract_mix_choices(self, value_text):
        return value_text.lower().strip() in ['yes', 'true', 'có', '1']

    def get_template_instructions(self):
        """Trả về hướng dẫn định dạng template"""
        return """
HƯỚNG DẪN ĐỊNH DẠNG FILE .DOCX (DẠNG BẢNG)

Mỗi câu hỏi phải nằm trong một bảng (Table) riêng biệt. Bảng phải có 2 cột.

- Cột 1: Chứa các nhãn (Label) như 'QN=1', 'a.', 'ANSWER:', 'MARK:'.
- Cột 2: Chứa nội dung tương ứng.

Cấu trúc một bảng câu hỏi mẫu:
|------------------|----------------------------------------------------|
|   **Cột 1 (Nhãn)** |   **Cột 2 (Nội dung)** |
|------------------|----------------------------------------------------|
| QN=1             | Nội dung câu hỏi [file:image.jpg]                  |
| a.               | Nội dung đáp án A                                  |
| b.               | Nội dung đáp án B                                  |
| c.               | Nội dung đáp án C                                  |
| d.               | Nội dung đáp án D                                  |
| ANSWER:          | B                                                  |
| MARK:            | 0.5                                                |
| UNIT:            | Chapter1                                           |
| MIX CHOICES:     | Yes                                                |
|------------------|----------------------------------------------------|

LƯU Ý:
- Mỗi câu hỏi phải là một bảng riêng.
- Các nhãn ở Cột 1 phải chính xác (ví dụ: 'QN=1', 'a.', 'ANSWER:').
- Để chèn hình ảnh, đặt placeholder `[file:tên_file_bất_kỳ.jpg]` vào nội dung câu hỏi.
- Hình ảnh sẽ được tự động trích xuất và liên kết. Thứ tự hình ảnh trong file phải khớp với thứ tự câu hỏi có hình ảnh.
"""

    def test_file_detailed(self, file_path):
        """Test file chi tiết - hiển thị từng dòng và lý do không nhận diện"""
        return False, "Chức năng test chi tiết chưa được cập nhật cho định dạng bảng."