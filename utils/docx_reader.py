from docx import Document
import re
import logging
from database.database_manager import DatabaseManager
import os
import base64
from io import BytesIO

class DocxReader:
    def __init__(self):
        self.db = DatabaseManager()
    
    def extract_images_from_docx(self, file_path):
        """Trích xuất hình ảnh từ file .docx"""
        try:
            doc = Document(file_path)
            images = []
            
            # Tìm hình ảnh trong paragraphs
            for i, paragraph in enumerate(doc.paragraphs):
                for run in paragraph.runs:
                    for element in run._element:
                        if element.tag.endswith('drawing'):
                            # Tìm hình ảnh trong drawing
                            for child in element.iter():
                                if child.tag.endswith('blip'):
                                    rId = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                    if rId:
                                        try:
                                            image_part = doc.part.related_parts[rId]
                                            image_data = image_part.blob
                                            image_name = f"image_{len(images) + 1}.png"
                                            images.append({
                                                'name': image_name,
                                                'data': image_data,
                                                'paragraph_index': i
                                            })
                                        except Exception as e:
                                            logging.warning(f"Không thể trích xuất hình ảnh: {e}")
            
            # Tìm hình ảnh trong headers/footers
            for section in doc.sections:
                for header in [section.header, section.first_page_header, section.even_page_header]:
                    if header:
                        for paragraph in header.paragraphs:
                            for run in paragraph.runs:
                                for element in run._element:
                                    if element.tag.endswith('drawing'):
                                        for child in element.iter():
                                            if child.tag.endswith('blip'):
                                                rId = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                                if rId:
                                                    try:
                                                        image_part = doc.part.related_parts[rId]
                                                        image_data = image_part.blob
                                                        image_name = f"header_image_{len(images) + 1}.png"
                                                        images.append({
                                                            'name': image_name,
                                                            'data': image_data,
                                                            'paragraph_index': -1
                                                        })
                                                    except Exception as e:
                                                        logging.warning(f"Không thể trích xuất hình ảnh header: {e}")
            
            logging.info(f"Trích xuất được {len(images)} hình ảnh từ file")
            return images
            
        except Exception as e:
            logging.error(f"Lỗi trích xuất hình ảnh: {e}")
            return []
    
    def save_images_to_folder(self, images, output_folder="extracted_images"):
        """Lưu hình ảnh vào thư mục"""
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            saved_images = []
            for i, image in enumerate(images):
                file_path = os.path.join(output_folder, image['name'])
                with open(file_path, 'wb') as f:
                    f.write(image['data'])
                saved_images.append({
                    'original_name': image['name'],
                    'file_path': file_path,
                    'paragraph_index': image['paragraph_index']
                })
                logging.info(f"Đã lưu hình ảnh: {file_path}")
            
            return saved_images
            
        except Exception as e:
            logging.error(f"Lỗi lưu hình ảnh: {e}")
            return []
    
    def extract_image_references_from_text(self, text):
        """Trích xuất tham chiếu hình ảnh từ text"""
        # Tìm pattern [file:filename.ext]
        pattern = r'\[file:([^\]]+)\]'
        matches = re.findall(pattern, text)
        return matches
    
    def process_text_with_images(self, text, images_info):
        """Xử lý text có chứa tham chiếu hình ảnh"""
        # Tìm tham chiếu hình ảnh trong text
        image_refs = self.extract_image_references_from_text(text)
        
        # Thay thế tham chiếu bằng thông tin hình ảnh thực tế
        processed_text = text
        for i, ref in enumerate(image_refs):
            # Tìm hình ảnh tương ứng
            image_info = None
            for img in images_info:
                if img['original_name'] == ref or f"image_{i+1}.png" == ref:
                    image_info = img
                    break
            
            if image_info:
                # Thay thế [file:filename] bằng thông tin hình ảnh
                replacement = f"[IMAGE: {image_info['file_path']}]"
                processed_text = processed_text.replace(f"[file:{ref}]", replacement)
            else:
                # Giữ nguyên tham chiếu nếu không tìm thấy hình ảnh
                logging.warning(f"Không tìm thấy hình ảnh: {ref}")
        
        return processed_text

    def test_file_detailed(self, file_path):
        """Test file chi tiết - hiển thị từng dòng và lý do không nhận diện"""
        try:
            if not os.path.exists(file_path):
                return False, f"File không tồn tại: {file_path}"
            
            if not file_path.lower().endswith('.docx'):
                return False, f"File không phải định dạng .docx: {file_path}"
            
            doc = Document(file_path)
            lines = []
            line_count = 0
            
            # Trích xuất hình ảnh
            images = self.extract_images_from_docx(file_path)
            saved_images = self.save_images_to_folder(images)
            
            for paragraph in doc.paragraphs:
                line_count += 1
                text = paragraph.text.strip()
                
                if not text:
                    continue
                
                # Xử lý text có hình ảnh
                processed_text = self.process_text_with_images(text, saved_images)
                
                # Phân tích từng dòng
                line_info = {
                    'line_number': line_count,
                    'text': text,
                    'processed_text': processed_text,
                    'is_question': False,
                    'is_option': False,
                    'is_answer': False,
                    'is_mark': False,
                    'is_unit': False,
                    'is_mix': False,
                    'has_image_ref': len(self.extract_image_references_from_text(text)) > 0,
                    'reason': ''
                }
                
                # Kiểm tra từng loại
                if self._is_question_start(text):
                    line_info['is_question'] = True
                    line_info['reason'] = '✅ Nhận diện là câu hỏi'
                elif self._is_option(text):
                    line_info['is_option'] = True
                    line_info['reason'] = '✅ Nhận diện là đáp án'
                elif self._is_correct_answer(text):
                    line_info['is_answer'] = True
                    line_info['reason'] = '✅ Nhận diện là đáp án đúng'
                elif self._is_mark_info(text):
                    line_info['is_mark'] = True
                    line_info['reason'] = '✅ Nhận diện là điểm'
                elif self._is_unit_info(text):
                    line_info['is_unit'] = True
                    line_info['reason'] = '✅ Nhận diện là đơn vị'
                elif self._is_mix_choices_info(text):
                    line_info['is_mix'] = True
                    line_info['reason'] = '✅ Nhận diện là trộn đáp án'
                else:
                    line_info['reason'] = '❌ Không nhận diện được định dạng'
                
                lines.append(line_info)
            
            # Thống kê
            questions_found = sum(1 for line in lines if line['is_question'])
            options_found = sum(1 for line in lines if line['is_option'])
            answers_found = sum(1 for line in lines if line['is_answer'])
            images_found = len(saved_images)
            
            # Tạo báo cáo chi tiết
            report = f"📋 BÁO CÁO CHI TIẾT FILE: {os.path.basename(file_path)}\n"
            report += f"📄 Tổng dòng: {len(lines)}\n"
            report += f"🖼️ Hình ảnh tìm thấy: {images_found}\n"
            report += f"❓ Câu hỏi tìm thấy: {questions_found}\n"
            report += f"🔤 Đáp án tìm thấy: {options_found}\n"
            report += f"✅ Đáp án đúng tìm thấy: {answers_found}\n\n"
            
            if images_found > 0:
                report += "🖼️ HÌNH ẢNH ĐÃ TRÍCH XUẤT:\n"
                for img in saved_images:
                    report += f"  📁 {img['file_path']}\n"
                report += "\n"
            
            if questions_found == 0:
                report += "⚠️ KHÔNG TÌM THẤY CÂU HỎI NÀO!\n"
                report += "Vui lòng kiểm tra định dạng file.\n\n"
            
            report += "📝 CHI TIẾT TỪNG DÒNG:\n"
            report += "=" * 60 + "\n"
            
            for line in lines:
                report += f"Dòng {line['line_number']}: '{line['text']}'\n"
                if line['has_image_ref']:
                    report += f"  🖼️ Có tham chiếu hình ảnh\n"
                if line['processed_text'] != line['text']:
                    report += f"  🔄 Sau xử lý: '{line['processed_text']}'\n"
                report += f"  → {line['reason']}\n"
                
                # Thêm thông tin debug cho câu hỏi
                if line['is_question']:
                    question_num = self._extract_question_number(line['text'])
                    report += f"  → Số câu hỏi: {question_num}\n"
                
                # Thêm thông tin debug cho đáp án
                if line['is_option']:
                    option_letter, option_text = self._extract_option(line['text'])
                    report += f"  → Đáp án {option_letter}: {option_text}\n"
                
                report += "\n"
            
            # Thêm gợi ý nếu không tìm thấy câu hỏi
            if questions_found == 0:
                report += "💡 GỢI Ý ĐỊNH DẠNG ĐÚNG:\n"
                report += "Câu hỏi phải bắt đầu bằng:\n"
                report += "- QN=1: Nội dung câu hỏi [file:image.jpg]\n"
                report += "- Câu 1: Nội dung câu hỏi [file:image.jpg]\n"
                report += "- 1. Nội dung câu hỏi [file:image.jpg]\n"
                report += "- Q1: Nội dung câu hỏi [file:image.jpg]\n\n"
                
                report += "Đáp án phải có định dạng:\n"
                report += "- a. Nội dung đáp án A\n"
                report += "- b. Nội dung đáp án B\n"
                report += "- c. Nội dung đáp án C\n"
                report += "- d. Nội dung đáp án D\n\n"
                
                report += "Đáp án đúng phải có định dạng:\n"
                report += "- ANSWER: A\n"
                report += "- Đáp án: B\n"
                report += "- Answer: C\n\n"
                
                report += "🖼️ HÌNH ẢNH:\n"
                report += "- Hình ảnh sẽ được tự động trích xuất\n"
                report += "- Tham chiếu [file:filename] sẽ được xử lý\n"
                report += "- Hình ảnh được lưu trong thư mục extracted_images/\n"
            
            return True, report
            
        except Exception as e:
            logging.error(f"Lỗi test file chi tiết: {e}")
            return False, f"Lỗi test file: {str(e)}"

    def read_docx_file(self, file_path, subject_id, creator_id):
        """Đọc file .docx và trích xuất câu hỏi (hỗ trợ hình ảnh)"""
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists(file_path):
                logging.error(f"File không tồn tại: {file_path}")
                return False, f"File không tồn tại: {file_path}"
            
            # Kiểm tra đuôi file
            if not file_path.lower().endswith('.docx'):
                logging.error(f"File không phải định dạng .docx: {file_path}")
                return False, f"File không phải định dạng .docx: {file_path}"
            
            logging.info(f"Bắt đầu đọc file: {file_path}")
            
            # Trích xuất hình ảnh
            images = self.extract_images_from_docx(file_path)
            saved_images = self.save_images_to_folder(images)
            logging.info(f"Đã trích xuất {len(saved_images)} hình ảnh")
            
            doc = Document(file_path)
            questions = []
            current_question = None
            line_count = 0
            
            logging.info(f"File có {len(doc.paragraphs)} paragraphs")
            
            for paragraph in doc.paragraphs:
                line_count += 1
                text = paragraph.text.strip()
                
                if not text:
                    continue
                
                # Xử lý text có hình ảnh
                processed_text = self.process_text_with_images(text, saved_images)
                
                logging.debug(f"Line {line_count}: '{text}' -> '{processed_text}'")
                
                # Kiểm tra định dạng câu hỏi
                if self._is_question_start(text):
                    # Lưu câu hỏi trước đó nếu có
                    if current_question and self._is_valid_question(current_question):
                        questions.append(current_question)
                        logging.info(f"Đã thêm câu hỏi: {current_question.get('question_number', 'Unknown')}")
                    
                    # Bắt đầu câu hỏi mới
                    question_number = self._extract_question_number(text)
                    current_question = {
                        'question_text': processed_text,  # Sử dụng text đã xử lý
                        'original_text': text,  # Lưu text gốc
                        'options': {},
                        'correct_answer': None,
                        'difficulty': 'medium',
                        'mark': 1.0,  # Điểm mặc định
                        'unit': '',   # Đơn vị bài học
                        'mix_choices': False,  # Có trộn đáp án không
                        'question_number': question_number,
                        'images': []  # Danh sách hình ảnh của câu hỏi
                    }
                    logging.info(f"Bắt đầu câu hỏi mới: {question_number}")
                
                elif current_question and self._is_option(text):
                    option_letter, option_text = self._extract_option(text)
                    if option_letter and option_text:
                        current_question['options'][option_letter] = option_text
                        logging.debug(f"Thêm đáp án {option_letter}: {option_text}")
                
                elif current_question and self._is_correct_answer(text):
                    correct_answer = self._extract_correct_answer(text)
                    if correct_answer:
                        current_question['correct_answer'] = correct_answer
                        logging.debug(f"Đáp án đúng: {correct_answer}")
                
                elif current_question and self._is_mark_info(text):
                    mark = self._extract_mark(text)
                    if mark is not None:
                        current_question['mark'] = mark
                        logging.debug(f"Điểm: {mark}")
                
                elif current_question and self._is_unit_info(text):
                    unit = self._extract_unit(text)
                    if unit:
                        current_question['unit'] = unit
                        logging.debug(f"Đơn vị: {unit}")
                
                elif current_question and self._is_mix_choices_info(text):
                    mix_choices = self._extract_mix_choices(text)
                    current_question['mix_choices'] = mix_choices
                    logging.debug(f"Trộn đáp án: {mix_choices}")
            
            # Thêm câu hỏi cuối cùng
            if current_question and self._is_valid_question(current_question):
                questions.append(current_question)
                logging.info(f"Đã thêm câu hỏi cuối: {current_question.get('question_number', 'Unknown')}")
            
            logging.info(f"Tổng câu hỏi đã parse: {len(questions)}")
            
            # Kiểm tra có câu hỏi nào không
            if not questions:
                logging.warning("Không tìm thấy câu hỏi hợp lệ nào trong file")
                return False, "Không tìm thấy câu hỏi hợp lệ nào trong file. Vui lòng kiểm tra định dạng."
            
            # Lưu vào cơ sở dữ liệu
            saved_count = 0
            for i, question in enumerate(questions):
                try:
                    if self._save_question_to_db(question, subject_id, creator_id):
                        saved_count += 1
                        logging.info(f"Đã lưu câu hỏi {i+1}/{len(questions)}")
                    else:
                        logging.error(f"Lỗi lưu câu hỏi {i+1}/{len(questions)}")
                except Exception as e:
                    logging.error(f"Lỗi lưu câu hỏi {i+1}: {e}")
            
            success_message = f"Đã đọc thành công {len(questions)} câu hỏi, lưu {saved_count} câu hỏi"
            if len(saved_images) > 0:
                success_message += f", trích xuất {len(saved_images)} hình ảnh"
            if saved_count < len(questions):
                success_message += f" ({len(questions) - saved_count} câu hỏi lỗi)"
            
            logging.info(success_message)
            return True, success_message
            
        except Exception as e:
            logging.error(f"Lỗi đọc file .docx: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            return False, f"Lỗi đọc file: {str(e)}"
    
    def _is_question_start(self, text):
        """Kiểm tra xem text có phải là bắt đầu câu hỏi không"""
        # Định dạng: "Câu 1:", "1.", "Q1:", "QN=1", etc.
        patterns = [
            r'^Câu\s+\d+[:.]',
            r'^\d+[:.]',
            r'^Q\d+[:.]',
            r'^QN\s*=\s*\d+[:.]',
            r'^Question\s+\d+[:.]',
            r'^QN\s*=\s*\d+',  # QN=1 format
            r'^Câu\s+\d+',     # Câu 1 format
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _extract_question_number(self, text):
        """Trích xuất số câu hỏi"""
        patterns = [
            r'QN\s*=\s*(\d+)',
            r'^Câu\s+(\d+)',
            r'^(\d+)[:.]',
            r'^Q(\d+)[:.]',
            r'^Question\s+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    def _is_option(self, text):
        """Kiểm tra xem text có phải là đáp án không"""
        # Định dạng: "a.", "b.", "c.", "d.", "a)", "b)", etc.
        patterns = [
            r'^[A-Da-d][:.)]',
            r'^[A-Da-d]\s+',  # a. hoặc A. với khoảng trắng
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        return False
    
    def _is_correct_answer(self, text):
        """Kiểm tra xem text có chứa đáp án đúng không"""
        # Định dạng: "ANSWER: B", "Đáp án: A", "Answer: B", etc.
        patterns = [
            r'^ANSWER[:.]\s*[A-Da-d]',
            r'^Đáp án[:.]\s*[A-Da-d]',
            r'^Answer[:.]\s*[A-Da-d]',
            r'^Correct[:.]\s*[A-Da-d]',
            r'^Đúng[:.]\s*[A-Da-d]'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_mark_info(self, text):
        """Kiểm tra xem text có chứa thông tin điểm không"""
        patterns = [
            r'^MARK[:.]\s*\d+\.?\d*',
            r'^Điểm[:.]\s*\d+\.?\d*',
            r'^Mark[:.]\s*\d+\.?\d*'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_unit_info(self, text):
        """Kiểm tra xem text có chứa thông tin đơn vị bài học không"""
        patterns = [
            r'^UNIT[:.]\s*\w+',
            r'^Đơn vị[:.]\s*\w+',
            r'^Unit[:.]\s*\w+',
            r'^Chapter[:.]\s*\w+'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_mix_choices_info(self, text):
        """Kiểm tra xem text có chứa thông tin trộn đáp án không"""
        patterns = [
            r'^MIX CHOICES[:.]\s*(Yes|No|True|False)',
            r'^Trộn đáp án[:.]\s*(Có|Không|Yes|No)',
            r'^Mix choices[:.]\s*(Yes|No|True|False)'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _extract_option(self, text):
        """Trích xuất chữ cái và nội dung đáp án"""
        # Hỗ trợ nhiều định dạng: "a.", "A.", "a)", "A)", "a. ", "A. "
        match = re.match(r'^([A-Da-d])[:.)]\s*(.+)$', text)
        if match:
            return match.group(1).upper(), match.group(2).strip()
        
        # Hỗ trợ định dạng: "a Nội dung" (không có dấu chấm)
        match = re.match(r'^([A-Da-d])\s+(.+)$', text)
        if match:
            return match.group(1).upper(), match.group(2).strip()
        
        return None, None
    
    def _extract_correct_answer(self, text):
        """Trích xuất đáp án đúng"""
        match = re.search(r'[A-Da-d]', text.upper())
        if match:
            return match.group().upper()
        return None
    
    def _extract_mark(self, text):
        """Trích xuất điểm số"""
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None
    
    def _extract_unit(self, text):
        """Trích xuất đơn vị bài học"""
        # Tìm phần sau dấu ":"
        match = re.search(r'[:.]\s*(.+)', text)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_mix_choices(self, text):
        """Trích xuất thông tin trộn đáp án"""
        text_lower = text.lower()
        if 'yes' in text_lower or 'true' in text_lower or 'có' in text_lower:
            return True
        elif 'no' in text_lower or 'false' in text_lower or 'không' in text_lower:
            return False
        return False
    
    def _is_valid_question(self, question):
        """Kiểm tra câu hỏi có hợp lệ không"""
        return (
            question['question_text'] and
            len(question['options']) >= 4 and
            question['correct_answer'] in ['A', 'B', 'C', 'D'] and
            question['correct_answer'] in question['options']
        )
    
    def _save_question_to_db(self, question, subject_id, creator_id):
        """Lưu câu hỏi vào cơ sở dữ liệu"""
        try:
            # Thêm thông tin bổ sung vào question_text
            additional_info = []
            if question.get('unit'):
                additional_info.append(f"Unit: {question['unit']}")
            if question.get('mark') and question['mark'] != 1.0:
                additional_info.append(f"Mark: {question['mark']}")
            if question.get('mix_choices'):
                additional_info.append("Mix Choices: Yes")
            
            # Thêm thông tin bổ sung vào cuối question_text
            full_question_text = question['question_text']
            if additional_info:
                full_question_text += f"\n[{' | '.join(additional_info)}]"
            
            query = """
                INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                subject_id,
                full_question_text,
                question['options'].get('A', ''),
                question['options'].get('B', ''),
                question['options'].get('C', ''),
                question['options'].get('D', ''),
                question['correct_answer'],
                question['difficulty'],
                creator_id
            )
            
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logging.error(f"Lỗi lưu câu hỏi: {e}")
            return False
    
    def get_template_instructions(self):
        """Trả về hướng dẫn định dạng template"""
        return """
HƯỚNG DẪN ĐỊNH DẠNG FILE .DOCX

1. Định dạng câu hỏi:
   - QN=1: Nội dung câu hỏi
   - Câu 1: Nội dung câu hỏi
   - 1. Nội dung câu hỏi
   - Q1: Nội dung câu hỏi

2. Định dạng câu hỏi có hình ảnh:
   - QN=1: Nội dung câu hỏi [file:image.jpg]
   - Câu 1: Nội dung câu hỏi [file:diagram.png]
   - 1. Nội dung câu hỏi [file:chart.jpg]

3. Định dạng đáp án:
   - a. Nội dung đáp án A
   - b. Nội dung đáp án B
   - c. Nội dung đáp án C
   - d. Nội dung đáp án D

4. Định dạng đáp án đúng:
   - ANSWER: A
   - Đáp án: B
   - Answer: C

5. Thông tin bổ sung (tùy chọn):
   - MARK: 0.5
   - UNIT: Chapter1
   - MIX CHOICES: Yes

6. Ví dụ hoàn chỉnh có hình ảnh:
   QN=1: See the figure and choose the right type of B2B E-Commerce [file:8435.jpg]
   a. Sell-side B2B
   b. Electronic Exchange
   c. Buy-side B2B
   d. Supply Chain Improvements and Collaborative Commerce
   ANSWER: B
   MARK: 0.5
   UNIT: Chapter1
   MIX CHOICES: Yes

7. Lưu ý về hình ảnh:
   - Hình ảnh sẽ được tự động trích xuất từ file .docx
   - Tham chiếu [file:filename] sẽ được xử lý
   - Hình ảnh được lưu trong thư mục extracted_images/
   - Hỗ trợ các định dạng: JPG, PNG, GIF, BMP
        """ 