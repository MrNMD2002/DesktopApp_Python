import json
import logging
from database.database_manager import DatabaseManager
from datetime import datetime

class QuestionManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_all_questions(self, subject_id=None, difficulty=None, active_only=True):
        """Lấy danh sách câu hỏi"""
        try:
            query = """
                SELECT q.*, s.name as subject_name, 
                       u1.full_name as created_by_name,
                       u2.full_name as updated_by_name
                FROM questions q
                JOIN subjects s ON q.subject_id = s.id
                JOIN users u1 ON q.created_by = u1.id
                LEFT JOIN users u2 ON q.updated_by = u2.id
                WHERE 1=1
            """
            params = []
            
            if active_only:
                query += " AND q.is_active = TRUE"
            
            if subject_id:
                query += " AND q.subject_id = %s"
                params.append(subject_id)
            
            if difficulty:
                query += " AND q.difficulty_level = %s"
                params.append(difficulty)
            
            query += " ORDER BY q.created_at DESC"
            
            result = self.db.execute_query(query, tuple(params))
            return result if result else []
        except Exception as e:
            logging.error(f"Lỗi lấy danh sách câu hỏi: {e}")
            return []
    
    def get_question_by_id(self, question_id):
        """Lấy thông tin câu hỏi theo ID"""
        try:
            query = """
                SELECT q.*, s.name as subject_name,
                       u1.full_name as created_by_name,
                       u2.full_name as updated_by_name
                FROM questions q
                JOIN subjects s ON q.subject_id = s.id
                JOIN users u1 ON q.created_by = u1.id
                LEFT JOIN users u2 ON q.updated_by = u2.id
                WHERE q.id = %s
            """
            result = self.db.execute_query(query, (question_id,))
            return result[0] if result else None
        except Exception as e:
            logging.error(f"Lỗi lấy câu hỏi: {e}")
            return None
    
    def create_question(self, subject_id, question_text, option_a, option_b, option_c, option_d, 
                       correct_answer, difficulty_level, created_by):
        """Tạo câu hỏi mới"""
        try:
            # Kiểm tra dữ liệu
            if not all([question_text, option_a, option_b, option_c, option_d, correct_answer]):
                return False, "Vui lòng điền đầy đủ thông tin"
            
            if correct_answer.upper() not in ['A', 'B', 'C', 'D']:
                return False, "Đáp án phải là A, B, C hoặc D"
            
            # Tạo câu hỏi
            insert_query = """
                INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d,
                                     correct_answer, difficulty_level, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(insert_query, (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_answer.upper(), difficulty_level, created_by
            ))
            
            # Lấy ID câu hỏi vừa tạo
            question_id = self.db.get_last_insert_id()
            
            # Lưu lịch sử
            self._save_history(question_id, 'created', None, {
                'subject_id': subject_id,
                'question_text': question_text,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,
                'correct_answer': correct_answer.upper(),
                'difficulty_level': difficulty_level
            }, created_by)
            
            logging.info(f"Tạo câu hỏi thành công: ID {question_id}")
            return True, "Tạo câu hỏi thành công"
        except Exception as e:
            logging.error(f"Lỗi tạo câu hỏi: {e}")
            return False, "Lỗi hệ thống"
    
    def update_question(self, question_id, subject_id, question_text, option_a, option_b, option_c, option_d,
                       correct_answer, difficulty_level, updated_by):
        """Cập nhật câu hỏi"""
        try:
            # Kiểm tra câu hỏi tồn tại
            question = self.get_question_by_id(question_id)
            if not question:
                return False, "Câu hỏi không tồn tại"
            
            # Kiểm tra dữ liệu
            if not all([question_text, option_a, option_b, option_c, option_d, correct_answer]):
                return False, "Vui lòng điền đầy đủ thông tin"
            
            if correct_answer.upper() not in ['A', 'B', 'C', 'D']:
                return False, "Đáp án phải là A, B, C hoặc D"
            
            # Lưu dữ liệu cũ để lịch sử
            old_data = {
                'subject_id': question['subject_id'],
                'question_text': question['question_text'],
                'option_a': question['option_a'],
                'option_b': question['option_b'],
                'option_c': question['option_c'],
                'option_d': question['option_d'],
                'correct_answer': question['correct_answer'],
                'difficulty_level': question['difficulty_level']
            }
            
            # Cập nhật câu hỏi
            update_query = """
                UPDATE questions 
                SET subject_id = %s, question_text = %s, option_a = %s, option_b = %s,
                    option_c = %s, option_d = %s, correct_answer = %s, difficulty_level = %s,
                    updated_by = %s, updated_at = NOW()
                WHERE id = %s
            """
            self.db.execute_query(update_query, (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_answer.upper(), difficulty_level, updated_by, question_id
            ))
            
            # Lưu lịch sử
            new_data = {
                'subject_id': subject_id,
                'question_text': question_text,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,
                'correct_answer': correct_answer.upper(),
                'difficulty_level': difficulty_level
            }
            self._save_history(question_id, 'updated', old_data, new_data, updated_by)
            
            logging.info(f"Cập nhật câu hỏi thành công: ID {question_id}")
            return True, "Cập nhật câu hỏi thành công"
        except Exception as e:
            logging.error(f"Lỗi cập nhật câu hỏi: {e}")
            return False, "Lỗi hệ thống"
    
    def delete_question(self, question_id, deleted_by):
        """Xóa câu hỏi (soft delete)"""
        try:
            # Kiểm tra câu hỏi tồn tại
            question = self.get_question_by_id(question_id)
            if not question:
                return False, "Câu hỏi không tồn tại"
            
            # Lưu dữ liệu cũ để lịch sử
            old_data = {
                'subject_id': question['subject_id'],
                'question_text': question['question_text'],
                'option_a': question['option_a'],
                'option_b': question['option_b'],
                'option_c': question['option_c'],
                'option_d': question['option_d'],
                'correct_answer': question['correct_answer'],
                'difficulty_level': question['difficulty_level']
            }
            
            # Soft delete
            delete_query = "UPDATE questions SET is_active = FALSE, updated_by = %s WHERE id = %s"
            self.db.execute_query(delete_query, (deleted_by, question_id))
            
            # Lưu lịch sử
            self._save_history(question_id, 'deleted', old_data, None, deleted_by)
            
            logging.info(f"Xóa câu hỏi thành công: ID {question_id}")
            return True, "Xóa câu hỏi thành công"
        except Exception as e:
            logging.error(f"Lỗi xóa câu hỏi: {e}")
            return False, "Lỗi hệ thống"
    
    def restore_question(self, question_id, restored_by):
        """Khôi phục câu hỏi đã xóa"""
        try:
            # Kiểm tra câu hỏi tồn tại và đã bị xóa
            query = "SELECT * FROM questions WHERE id = %s AND is_active = FALSE"
            result = self.db.execute_query(query, (question_id,))
            
            if not result:
                return False, "Câu hỏi không tồn tại hoặc chưa bị xóa"
            
            question = result[0]
            
            # Khôi phục
            restore_query = "UPDATE questions SET is_active = TRUE, updated_by = %s WHERE id = %s"
            self.db.execute_query(restore_query, (restored_by, question_id))
            
            # Lưu lịch sử
            old_data = {
                'subject_id': question['subject_id'],
                'question_text': question['question_text'],
                'option_a': question['option_a'],
                'option_b': question['option_b'],
                'option_c': question['option_c'],
                'option_d': question['option_d'],
                'correct_answer': question['correct_answer'],
                'difficulty_level': question['difficulty_level']
            }
            self._save_history(question_id, 'restored', None, old_data, restored_by)
            
            logging.info(f"Khôi phục câu hỏi thành công: ID {question_id}")
            return True, "Khôi phục câu hỏi thành công"
        except Exception as e:
            logging.error(f"Lỗi khôi phục câu hỏi: {e}")
            return False, "Lỗi hệ thống"
    
    def get_question_history(self, question_id):
        """Lấy lịch sử chỉnh sửa câu hỏi"""
        try:
            query = """
                SELECT h.*, u.full_name as changed_by_name
                FROM question_history h
                JOIN users u ON h.changed_by = u.id
                WHERE h.question_id = %s
                ORDER BY h.changed_at DESC
            """
            result = self.db.execute_query(query, (question_id,))
            return result if result else []
        except Exception as e:
            logging.error(f"Lỗi lấy lịch sử câu hỏi: {e}")
            return []
    
    def get_all_question_history(self, limit=100):
        """Lấy tất cả lịch sử chỉnh sửa câu hỏi (chỉ admin)"""
        try:
            query = """
                SELECT h.*, q.question_text, s.name as subject_name, u.full_name as changed_by_name
                FROM question_history h
                JOIN questions q ON h.question_id = q.id
                JOIN subjects s ON q.subject_id = s.id
                JOIN users u ON h.changed_by = u.id
                ORDER BY h.changed_at DESC
                LIMIT %s
            """
            result = self.db.execute_query(query, (limit,))
            return result if result else []
        except Exception as e:
            logging.error(f"Lỗi lấy lịch sử câu hỏi: {e}")
            return []
    
    def get_question_history_by_user(self, user_id, limit=100):
        """Lấy lịch sử chỉnh sửa câu hỏi theo user (cho giáo viên)"""
        try:
            query = """
                SELECT h.*, q.question_text, s.name as subject_name, u.full_name as changed_by_name
                FROM question_history h
                JOIN questions q ON h.question_id = q.id
                JOIN subjects s ON q.subject_id = s.id
                JOIN users u ON h.changed_by = u.id
                WHERE h.changed_by = %s
                ORDER BY h.changed_at DESC
                LIMIT %s
            """
            result = self.db.execute_query(query, (user_id, limit))
            return result if result else []
        except Exception as e:
            logging.error(f"Lỗi lấy lịch sử câu hỏi theo user: {e}")
            return []
    
    def _save_history(self, question_id, action, old_data, new_data, changed_by):
        """Lưu lịch sử chỉnh sửa"""
        try:
            insert_query = """
                INSERT INTO question_history (question_id, action, old_data, new_data, changed_by)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            old_json = json.dumps(old_data, ensure_ascii=False) if old_data else None
            new_json = json.dumps(new_data, ensure_ascii=False) if new_data else None
            
            self.db.execute_query(insert_query, (
                question_id, action, old_json, new_json, changed_by
            ))
        except Exception as e:
            logging.error(f"Lỗi lưu lịch sử: {e}")
    
    def get_question_statistics(self):
        """Lấy thống kê câu hỏi"""
        try:
            query = """
                SELECT 
                    s.name as subject_name,
                    COUNT(CASE WHEN q.is_active = TRUE THEN 1 END) as active_count,
                    COUNT(CASE WHEN q.is_active = FALSE THEN 1 END) as deleted_count,
                    COUNT(CASE WHEN q.difficulty_level = 'easy' THEN 1 END) as easy_count,
                    COUNT(CASE WHEN q.difficulty_level = 'medium' THEN 1 END) as medium_count,
                    COUNT(CASE WHEN q.difficulty_level = 'hard' THEN 1 END) as hard_count
                FROM subjects s
                LEFT JOIN questions q ON s.id = q.subject_id
                GROUP BY s.id, s.name
                ORDER BY s.name
            """
            result = self.db.execute_query(query)
            return result if result else []
        except Exception as e:
            logging.error(f"Lỗi lấy thống kê câu hỏi: {e}")
            return [] 