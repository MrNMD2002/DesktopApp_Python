#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ tạo đề thi tự động từ câu hỏi đã import
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager import DatabaseManager
import random

class ExamCreator:
    def __init__(self):
        self.db = DatabaseManager()
    
    def check_questions_availability(self):
        """Kiểm tra số lượng câu hỏi có sẵn"""
        print("=" * 80)
        print("🔍 KIỂM TRA CÂU HỎI TRONG DATABASE")
        print("=" * 80)
        
        try:
            # Kiểm tra tổng số câu hỏi
            total_query = "SELECT COUNT(*) as count FROM questions WHERE is_active = TRUE"
            total_result = self.db.execute_query(total_query)
            total_questions = total_result[0]['count'] if total_result else 0
            
            print(f"📊 Tổng số câu hỏi: {total_questions}")
            
            if total_questions == 0:
                print("❌ Không có câu hỏi nào trong database!")
                print("💡 Hãy import câu hỏi từ file Word trước")
                return False
            
            # Kiểm tra câu hỏi theo môn học
            subject_query = """
                SELECT s.name, COUNT(q.id) as count
                FROM subjects s
                LEFT JOIN questions q ON s.id = q.subject_id AND q.is_active = TRUE
                GROUP BY s.id, s.name
                ORDER BY s.name
            """
            subjects = self.db.execute_query(subject_query)
            
            print("\n📚 CÂU HỎI THEO MÔN HỌC:")
            for subject in subjects:
                print(f"   {subject['name']}: {subject['count']} câu hỏi")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi kiểm tra: {e}")
            return False
    
    def check_existing_exams(self):
        """Kiểm tra đề thi đã có"""
        print("\n" + "=" * 80)
        print("📋 KIỂM TRA ĐỀ THI ĐÃ CÓ")
        print("=" * 80)
        
        try:
            query = """
                SELECT e.exam_code, e.title, s.name as subject_name, 
                       e.total_questions, e.created_at
                FROM exams e
                JOIN subjects s ON e.subject_id = s.id
                ORDER BY e.created_at DESC
            """
            exams = self.db.execute_query(query)
            
            if not exams:
                print("📝 Chưa có đề thi nào")
                return []
            
            print(f"📝 Tìm thấy {len(exams)} đề thi:")
            for exam in exams:
                created_date = exam['created_at'].strftime('%d/%m/%Y %H:%M')
                print(f"   {exam['exam_code']}: {exam['title']} ({exam['subject_name']}) - {exam['total_questions']} câu - {created_date}")
            
            return exams
            
        except Exception as e:
            print(f"❌ Lỗi kiểm tra đề thi: {e}")
            return []
    
    def create_sample_exams(self):
        """Tạo đề thi mẫu tự động"""
        print("\n" + "=" * 80)
        print("🎯 TẠO ĐỀ THI MẪU TỰ ĐỘNG")
        print("=" * 80)
        
        try:
            # Lấy danh sách môn học có câu hỏi
            subject_query = """
                SELECT s.id, s.name, COUNT(q.id) as count
                FROM subjects s
                JOIN questions q ON s.id = q.subject_id AND q.is_active = TRUE
                GROUP BY s.id, s.name
                HAVING COUNT(q.id) >= 5
                ORDER BY s.name
            """
            subjects = self.db.execute_query(subject_query)
            
            if not subjects:
                print("❌ Không có môn học nào đủ câu hỏi để tạo đề thi!")
                print("💡 Cần ít nhất 5 câu hỏi cho mỗi môn học")
                return False
            
            created_exams = []
            
            for subject in subjects:
                subject_id = subject['id']
                subject_name = subject['name']
                available_questions = subject['count']
                
                print(f"\n📚 Tạo đề thi cho môn: {subject_name}")
                print(f"   Số câu hỏi có sẵn: {available_questions}")
                
                # Tạo 2 đề thi cho mỗi môn học
                for i in range(1, 3):
                    # Tính số câu hỏi cho đề thi (tối đa 20, tối thiểu 5)
                    question_count = min(20, max(5, available_questions // 2))
                    
                    # Tạo mã đề thi
                    exam_code = f"{subject_name.upper()[:3]}{i:02d}"
                    
                    # Tạo tên đề thi
                    exam_title = f"Đề thi {subject_name} - Lần {i}"
                    
                    # Thời gian làm bài (1 phút/câu)
                    duration = question_count
                    
                    # Kiểm tra mã đề đã tồn tại chưa
                    check_query = "SELECT id FROM exams WHERE exam_code = %s"
                    existing = self.db.execute_query(check_query, (exam_code,))
                    
                    if existing:
                        print(f"   ⚠️ Mã đề {exam_code} đã tồn tại, bỏ qua")
                        continue
                    
                    # Tạo đề thi
                    insert_query = """
                        INSERT INTO exams (exam_code, subject_id, title, duration, total_questions, created_by)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    # Sử dụng admin làm người tạo
                    admin_query = "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
                    admin_result = self.db.execute_query(admin_query)
                    creator_id = admin_result[0]['id'] if admin_result else 1
                    
                    self.db.execute_query(insert_query, (
                        exam_code, subject_id, exam_title, duration, question_count, creator_id
                    ))
                    
                    exam_id = self.db.get_last_insert_id()
                    
                    # Chọn câu hỏi ngẫu nhiên
                    questions_query = """
                        SELECT id FROM questions 
                        WHERE subject_id = %s AND is_active = TRUE
                        ORDER BY RAND() 
                        LIMIT %s
                    """
                    questions = self.db.execute_query(questions_query, (subject_id, question_count))
                    
                    # Thêm câu hỏi vào đề thi
                    exam_questions_query = """
                        INSERT INTO exam_questions (exam_id, question_id, question_order)
                        VALUES (%s, %s, %s)
                    """
                    
                    for j, question in enumerate(questions):
                        self.db.execute_query(exam_questions_query, (exam_id, question['id'], j + 1))
                    
                    created_exams.append({
                        'code': exam_code,
                        'title': exam_title,
                        'subject': subject_name,
                        'questions': question_count,
                        'duration': duration
                    })
                    
                    print(f"   ✅ Đã tạo đề thi: {exam_code} - {question_count} câu - {duration} phút")
            
            if created_exams:
                print(f"\n🎉 Đã tạo thành công {len(created_exams)} đề thi!")
                print("\n📋 DANH SÁCH ĐỀ THI ĐÃ TẠO:")
                for exam in created_exams:
                    print(f"   {exam['code']}: {exam['title']} ({exam['subject']}) - {exam['questions']} câu - {exam['duration']} phút")
                
                return True
            else:
                print("❌ Không tạo được đề thi nào!")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi tạo đề thi: {e}")
            return False
    
    def show_student_instructions(self):
        """Hiển thị hướng dẫn cho học sinh"""
        print("\n" + "=" * 80)
        print("👨‍🎓 HƯỚNG DẪN CHO HỌC SINH")
        print("=" * 80)
        
        print("📋 Để học sinh có thể làm bài thi:")
        print("1. Đăng nhập với tài khoản học sinh (student1)")
        print("2. Chọn đề thi từ danh sách có sẵn")
        print("3. Bắt đầu làm bài thi")
        print("4. Nộp bài và xem điểm")
        
        print("\n🔑 TÀI KHOẢN MẪU:")
        print("   Username: student1")
        print("   Password: 123456")
        
        print("\n🎯 TÀI KHOẢN TẠO ĐỀ THI:")
        print("   Username: admin")
        print("   Password: 123456")
        print("   Vào menu: Quản lý đề thi")
    
    def main(self):
        """Hàm main"""
        print("🚀 CÔNG CỤ TẠO ĐỀ THI TỰ ĐỘNG")
        print("=" * 80)
        
        # Kiểm tra câu hỏi
        if not self.check_questions_availability():
            return
        
        # Kiểm tra đề thi hiện có
        existing_exams = self.check_existing_exams()
        
        if existing_exams:
            print(f"\n💡 Đã có {len(existing_exams)} đề thi")
            choice = input("Bạn có muốn tạo thêm đề thi mẫu không? (y/n): ").strip().lower()
            if choice != 'y':
                self.show_student_instructions()
                return
        
        # Tạo đề thi mẫu
        if self.create_sample_exams():
            self.show_student_instructions()
        else:
            print("\n❌ Không thể tạo đề thi!")
            print("💡 Hãy kiểm tra lại câu hỏi trong database")

def main():
    """Hàm main"""
    creator = ExamCreator()
    creator.main()

if __name__ == "__main__":
    main() 