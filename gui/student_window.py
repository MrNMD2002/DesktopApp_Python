import tkinter as tk
from tkinter import ttk, messagebox
from database.database_manager import DatabaseManager
import datetime

class StudentWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db = DatabaseManager()
        self.current_exam = None
        self.current_question_index = 0
        self.answers = {}
        self.start_time = None
        self.setup_ui()
        self.load_available_exams()
    
    def setup_ui(self):
        """Thiết lập giao diện học sinh"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Học sinh - Hệ thống Quản lý Đề thi")
        self.window.geometry("800x600")
        
        # Frame chính
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        user_info = self.auth_manager.get_current_user()
        ttk.Label(header_frame, text=f"Chào mừng: {user_info['full_name']}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame chọn đề thi
        self.exam_selection_frame = ttk.LabelFrame(self.main_frame, text="Chọn đề thi", padding="10")
        self.exam_selection_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Danh sách đề thi
        ttk.Label(self.exam_selection_frame, text="Đề thi có sẵn:").grid(row=0, column=0, sticky="w")
        
        # Treeview cho danh sách đề thi
        columns = ("Mã đề", "Tên đề", "Môn học", "Thời gian", "Số câu")
        self.exam_tree = ttk.Treeview(self.exam_selection_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.exam_tree.heading(col, text=col)
            self.exam_tree.column(col, width=120)
        
        self.exam_tree.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Scrollbar cho treeview
        scrollbar = ttk.Scrollbar(self.exam_selection_frame, orient="vertical", command=self.exam_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.exam_tree.configure(yscrollcommand=scrollbar.set)
        
        # Nút bắt đầu làm bài
        ttk.Button(self.exam_selection_frame, text="Bắt đầu làm bài", 
                  command=self.start_exam).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame làm bài thi (ẩn ban đầu)
        self.exam_frame = ttk.LabelFrame(self.main_frame, text="Làm bài thi", padding="10")
        
        # Thông tin đề thi
        self.exam_info_frame = ttk.Frame(self.exam_frame)
        self.exam_info_frame.pack(fill="x", pady=(0, 10))
        
        self.exam_title_label = ttk.Label(self.exam_info_frame, text="", font=("Arial", 12, "bold"))
        self.exam_title_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(self.exam_info_frame, text="", font=("Arial", 10))
        self.time_label.pack(side=tk.RIGHT)
        
        # Frame câu hỏi
        self.question_frame = ttk.Frame(self.exam_frame)
        self.question_frame.pack(fill="both", expand=True, pady=10)
        
        self.question_text = tk.Text(self.question_frame, height=6, wrap="word", state="disabled")
        self.question_text.pack(fill="x", pady=(0, 10))
        
        # Frame đáp án
        self.options_frame = ttk.Frame(self.question_frame)
        self.options_frame.pack(fill="x")
        
        self.answer_var = tk.StringVar()
        self.option_buttons = {}
        
        for i, option in enumerate(['A', 'B', 'C', 'D']):
            btn = ttk.Radiobutton(self.options_frame, text="", variable=self.answer_var, 
                                 value=option, command=self.save_answer)
            btn.grid(row=i, column=0, sticky="w", pady=2)
            self.option_buttons[option] = btn
        
        # Frame điều hướng
        navigation_frame = ttk.Frame(self.exam_frame)
        navigation_frame.pack(fill="x", pady=10)
        
        ttk.Button(navigation_frame, text="Câu trước", 
                  command=self.previous_question).pack(side=tk.LEFT)
        
        self.question_counter_label = ttk.Label(navigation_frame, text="")
        self.question_counter_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(navigation_frame, text="Câu tiếp", 
                  command=self.next_question).pack(side=tk.LEFT)
        
        ttk.Button(navigation_frame, text="Nộp bài", 
                  command=self.submit_exam).pack(side=tk.RIGHT)
        
        # Bind events
        self.exam_tree.bind("<Double-1>", lambda e: self.start_exam())
    
    def load_available_exams(self):
        """Tải danh sách đề thi có sẵn"""
        try:
            query = """
                SELECT e.exam_code, e.title, s.name as subject_name, 
                       e.duration, e.total_questions, e.id
                FROM exams e
                JOIN subjects s ON e.subject_id = s.id
                WHERE e.id NOT IN (
                    SELECT exam_id FROM student_exams 
                    WHERE student_id = %s AND status = 'completed'
                )
            """
            exams = self.db.execute_query(query, (self.auth_manager.get_current_user()['id'],))
            
            # Xóa dữ liệu cũ
            for item in self.exam_tree.get_children():
                self.exam_tree.delete(item)
            
            # Thêm dữ liệu mới
            for exam in exams:
                self.exam_tree.insert("", "end", values=(
                    exam['exam_code'],
                    exam['title'],
                    exam['subject_name'],
                    f"{exam['duration']} phút",
                    exam['total_questions']
                ), tags=(exam['id'],))
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách đề thi: {str(e)}")
    
    def start_exam(self):
        """Bắt đầu làm bài thi"""
        selection = self.exam_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đề thi!")
            return
        
        exam_id = self.exam_tree.item(selection[0], "tags")[0]
        
        try:
            # Lấy thông tin đề thi
            query = """
                SELECT e.*, s.name as subject_name
                FROM exams e
                JOIN subjects s ON e.subject_id = s.id
                WHERE e.id = %s
            """
            exam_info = self.db.execute_query(query, (exam_id,))
            
            if not exam_info:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin đề thi!")
                return
            
            self.current_exam = exam_info[0]
            
            # Lấy danh sách câu hỏi
            query = """
                SELECT q.* FROM questions q
                JOIN exam_questions eq ON q.id = eq.question_id
                WHERE eq.exam_id = %s
                ORDER BY eq.question_order
            """
            self.questions = self.db.execute_query(query, (exam_id,))
            
            if not self.questions:
                messagebox.showerror("Lỗi", "Đề thi không có câu hỏi!")
                return
            
            # Tạo bản ghi bài thi
            student_id = self.auth_manager.get_current_user()['id']
            insert_query = """
                INSERT INTO student_exams (student_id, exam_id, start_time)
                VALUES (%s, %s, NOW())
            """
            self.db.execute_query(insert_query, (student_id, exam_id))
            self.student_exam_id = self.db.get_last_insert_id()
            
            # Khởi tạo
            self.current_question_index = 0
            self.answers = {}
            self.start_time = datetime.datetime.now()
            
            # Hiển thị giao diện làm bài
            self.exam_selection_frame.grid_remove()
            self.exam_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
            
            # Hiển thị câu hỏi đầu tiên
            self.display_question()
            
            # Bắt đầu đếm thời gian
            self.update_timer()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể bắt đầu bài thi: {str(e)}")
    
    def display_question(self):
        """Hiển thị câu hỏi hiện tại"""
        if not self.questions or self.current_question_index >= len(self.questions):
            return
        
        question = self.questions[self.current_question_index]
        
        # Cập nhật thông tin đề thi
        if self.current_exam:
            self.exam_title_label.config(text=f"{self.current_exam['title']} - {self.current_exam['subject_name']}")
        
        # Hiển thị câu hỏi
        self.question_text.config(state="normal")
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"Câu {self.current_question_index + 1}: {question['question_text']}")
        self.question_text.config(state="disabled")
        
        # Hiển thị đáp án
        options = [
            ('A', question['option_a']),
            ('B', question['option_b']),
            ('C', question['option_c']),
            ('D', question['option_d'])
        ]
        
        for option, text in options:
            self.option_buttons[option].config(text=f"{option}. {text}")
        
        # Cập nhật câu trả lời đã chọn
        question_id = question['id']
        if question_id in self.answers:
            self.answer_var.set(self.answers[question_id])
        else:
            self.answer_var.set("")
        
        # Cập nhật số câu
        self.question_counter_label.config(
            text=f"Câu {self.current_question_index + 1}/{len(self.questions)}"
        )
    
    def save_answer(self):
        """Lưu câu trả lời"""
        if not self.questions or self.current_question_index >= len(self.questions):
            return
        
        question_id = self.questions[self.current_question_index]['id']
        selected_answer = self.answer_var.get()
        
        if selected_answer:
            self.answers[question_id] = selected_answer
    
    def next_question(self):
        """Chuyển đến câu hỏi tiếp theo"""
        self.save_answer()
        
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
    
    def previous_question(self):
        """Chuyển đến câu hỏi trước"""
        self.save_answer()
        
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question()
    
    def update_timer(self):
        """Cập nhật thời gian làm bài"""
        if not self.start_time or not self.current_exam:
            return
        
        elapsed = datetime.datetime.now() - self.start_time
        remaining = datetime.timedelta(minutes=self.current_exam['duration']) - elapsed
        
        if remaining.total_seconds() <= 0:
            self.submit_exam()
            return
        
        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)
        self.time_label.config(text=f"Thời gian còn lại: {minutes:02d}:{seconds:02d}")
        
        # Cập nhật mỗi giây
        self.window.after(1000, self.update_timer)
    
    def submit_exam(self):
        """Nộp bài thi"""
        self.save_answer()
        
        if not self.answers:
            messagebox.showwarning("Cảnh báo", "Bạn chưa trả lời câu hỏi nào!")
            return
        
        try:
            # Tính điểm
            correct_count = 0
            total_questions = len(self.questions)
            
            for question in self.questions:
                question_id = question['id']
                if question_id in self.answers:
                    selected_answer = self.answers[question_id]
                    is_correct = selected_answer == question['correct_answer']
                    
                    if is_correct:
                        correct_count += 1
                    
                    # Lưu câu trả lời
                    insert_query = """
                        INSERT INTO student_answers (student_exam_id, question_id, selected_answer, is_correct)
                        VALUES (%s, %s, %s, %s)
                    """
                    self.db.execute_query(insert_query, (
                        self.student_exam_id, question_id, selected_answer, is_correct
                    ))
            
            # Tính điểm (thang điểm 10)
            score = (correct_count / total_questions) * 10
            
            # Cập nhật trạng thái bài thi
            update_query = """
                UPDATE student_exams 
                SET end_time = NOW(), score = %s, status = 'completed'
                WHERE id = %s
            """
            self.db.execute_query(update_query, (score, self.student_exam_id))
            
            # Hiển thị kết quả
            messagebox.showinfo("Kết quả", 
                              f"Điểm của bạn: {score:.2f}/10\n"
                              f"Số câu đúng: {correct_count}/{total_questions}")
            
            # Quay lại màn hình chọn đề thi
            self.back_to_exam_selection()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nộp bài: {str(e)}")
    
    def back_to_exam_selection(self):
        """Quay lại màn hình chọn đề thi"""
        self.exam_frame.grid_remove()
        self.exam_selection_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.load_available_exams()
    
    def logout(self):
        """Đăng xuất"""
        self.auth_manager.logout()
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 