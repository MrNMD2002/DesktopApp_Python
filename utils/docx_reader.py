from docx import Document
import re
import logging
from database.database_manager import DatabaseManager

class DocxReader:
    def __init__(self):
        self.db = DatabaseManager()
    
    def read_docx_file(self, file_path, subject_id, creator_id):
        """Đọc file .docx và trích xuất câu hỏi"""
        try:
            doc = Document(file_path)
            questions = []
            current_question = None
            
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                
                # Kiểm tra định dạng câu hỏi
                if self._is_question_start(text):
                    # Lưu câu hỏi trước đó nếu có
                    if current_question and self._is_valid_question(current_question):
                        questions.append(current_question)
                    
                    # Bắt đầu câu hỏi mới
                    current_question = {
                        'question_text': text,
                        'options': {},
                        'correct_answer': None,
                        'difficulty': 'medium'
                    }
                
                elif current_question and self._is_option(text):
                    option_letter, option_text = self._extract_option(text)
                    if option_letter and option_text:
                        current_question['options'][option_letter] = option_text
                
                elif current_question and self._is_correct_answer(text):
                    correct_answer = self._extract_correct_answer(text)
                    if correct_answer:
                        current_question['correct_answer'] = correct_answer
            
            # Thêm câu hỏi cuối cùng
            if current_question and self._is_valid_question(current_question):
                questions.append(current_question)
            
            # Lưu vào cơ sở dữ liệu
            saved_count = 0
            for question in questions:
                if self._save_question_to_db(question, subject_id, creator_id):
                    saved_count += 1
            
            return True, f"Đã đọc thành công {len(questions)} câu hỏi, lưu {saved_count} câu hỏi"
            
        except Exception as e:
            logging.error(f"Lỗi đọc file .docx: {e}")
            return False, f"Lỗi đọc file: {str(e)}"
    
    def _is_question_start(self, text):
        """Kiểm tra xem text có phải là bắt đầu câu hỏi không"""
        # Định dạng: "Câu 1:", "1.", "Q1:", etc.
        patterns = [
            r'^Câu\s+\d+[:.]',
            r'^\d+[:.]',
            r'^Q\d+[:.]',
            r'^Question\s+\d+[:.]'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_option(self, text):
        """Kiểm tra xem text có phải là đáp án không"""
        # Định dạng: "A.", "B.", "C.", "D.", "a)", "b)", etc.
        patterns = [
            r'^[A-D][:.)]',
            r'^[a-d][:.)]'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        return False
    
    def _is_correct_answer(self, text):
        """Kiểm tra xem text có chứa đáp án đúng không"""
        # Định dạng: "Đáp án: A", "Answer: B", "Correct: C", etc.
        patterns = [
            r'^Đáp án[:.]\s*[A-D]',
            r'^Answer[:.]\s*[A-D]',
            r'^Correct[:.]\s*[A-D]',
            r'^Đúng[:.]\s*[A-D]'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _extract_option(self, text):
        """Trích xuất chữ cái và nội dung đáp án"""
        match = re.match(r'^([A-Da-d])[:.)]\s*(.+)$', text)
        if match:
            return match.group(1).upper(), match.group(2).strip()
        return None, None
    
    def _extract_correct_answer(self, text):
        """Trích xuất đáp án đúng"""
        match = re.search(r'[A-D]', text.upper())
        if match:
            return match.group()
        return None
    
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
            query = """
                INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                subject_id,
                question['question_text'],
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
   - Câu 1: Nội dung câu hỏi
   - 1. Nội dung câu hỏi
   - Q1: Nội dung câu hỏi

2. Định dạng đáp án:
   - A. Nội dung đáp án A
   - B. Nội dung đáp án B
   - C. Nội dung đáp án C
   - D. Nội dung đáp án D

3. Định dạng đáp án đúng:
   - Đáp án: A
   - Answer: B
   - Correct: C

4. Ví dụ:
   Câu 1: Thủ đô của Việt Nam là?
   A. Hà Nội
   B. TP. Hồ Chí Minh
   C. Đà Nẵng
   D. Huế
   Đáp án: A
        """ 