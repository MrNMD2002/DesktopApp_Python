import tkinter as tk
from tkinter import ttk, messagebox
from database.database_manager import DatabaseManager
import random

class ExamGeneratorWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db = DatabaseManager()
        self.setup_ui()
        self.load_subjects()
        self.load_exams()
    
    def setup_ui(self):
        """Thiết lập giao diện người sinh đề"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Người sinh đề - Hệ thống Quản lý Đề thi")
        self.window.geometry("800x600")
        
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        user_info = self.auth_manager.get_current_user()
        ttk.Label(header_frame, text=f"Chào mừng: {user_info['full_name']}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame tạo đề thi mới
        create_frame = ttk.LabelFrame(main_frame, text="Tạo đề thi mới", padding="10")
        create_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Mã đề
        ttk.Label(create_frame, text="Mã đề:").grid(row=0, column=0, sticky="w", pady=2)
        self.exam_code_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.exam_code_var, width=20).grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # Tên đề
        ttk.Label(create_frame, text="Tên đề:").grid(row=0, column=2, sticky="w", padx=(20, 0), pady=2)
        self.exam_title_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.exam_title_var, width=30).grid(row=0, column=3, padx=(10, 0), sticky="w")
        
        # Môn học
        ttk.Label(create_frame, text="Môn học:").grid(row=1, column=0, sticky="w", pady=2)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(create_frame, textvariable=self.subject_var, 
                                         state="readonly", width=20)
        self.subject_combo.grid(row=1, column=1, padx=(10, 0), sticky="w")
        
        # Số câu hỏi
        ttk.Label(create_frame, text="Số câu hỏi:").grid(row=1, column=2, sticky="w", padx=(20, 0), pady=2)
        self.question_count_var = tk.StringVar(value="20")
        ttk.Entry(create_frame, textvariable=self.question_count_var, width=10).grid(row=1, column=3, padx=(10, 0), sticky="w")
        
        # Thời gian làm bài
        ttk.Label(create_frame, text="Thời gian (phút):").grid(row=2, column=0, sticky="w", pady=2)
        self.duration_var = tk.StringVar(value="30")
        ttk.Entry(create_frame, textvariable=self.duration_var, width=10).grid(row=2, column=1, padx=(10, 0), sticky="w")
        
        # Nút tạo đề
        ttk.Button(create_frame, text="Tạo đề thi", 
                  command=self.create_exam).grid(row=2, column=2, columnspan=2, padx=(20, 0), pady=10)
        
        # Frame danh sách đề thi
        exams_frame = ttk.LabelFrame(main_frame, text="Danh sách đề thi", padding="10")
        exams_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # Treeview cho danh sách đề thi
        columns = ("Mã đề", "Tên đề", "Môn học", "Thời gian", "Số câu", "Ngày tạo")
        self.exams_tree = ttk.Treeview(exams_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.exams_tree.heading(col, text=col)
            self.exams_tree.column(col, width=120)
        
        self.exams_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(exams_frame, orient="vertical", command=self.exams_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.exams_tree.configure(yscrollcommand=scrollbar.set)
        
        # Nút xem chi tiết và xóa
        button_frame = ttk.Frame(exams_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Xem chi tiết", 
                  command=self.view_exam_details).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Xóa đề thi", 
                  command=self.delete_exam).pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Làm mới", 
                  command=self.load_exams).pack(side=tk.RIGHT)
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        exams_frame.columnconfigure(0, weight=1)
        exams_frame.rowconfigure(0, weight=1)
        create_frame.columnconfigure(3, weight=1)
    
    def load_subjects(self):
        """Tải danh sách môn học"""
        try:
            query = "SELECT id, name FROM subjects ORDER BY name"
            subjects = self.db.execute_query(query)
            
            subject_dict = {}
            subject_names = []
            
            for subject in subjects:
                subject_dict[subject['name']] = subject['id']
                subject_names.append(subject['name'])
            
            self.subject_combo['values'] = subject_names
            self.subject_dict = subject_dict
            
            if subject_names:
                self.subject_combo.set(subject_names[0])
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")
    
    def load_exams(self):
        """Tải danh sách đề thi"""
        try:
            query = """
                SELECT e.exam_code, e.title, s.name as subject_name, 
                       e.duration, e.total_questions, e.created_at, e.id
                FROM exams e
                JOIN subjects s ON e.subject_id = s.id
                ORDER BY e.created_at DESC
            """
            exams = self.db.execute_query(query)
            
            # Xóa dữ liệu cũ
            for item in self.exams_tree.get_children():
                self.exams_tree.delete(item)
            
            # Thêm dữ liệu mới
            for exam in exams:
                created_date = exam['created_at'].strftime('%d/%m/%Y %H:%M')
                self.exams_tree.insert("", "end", values=(
                    exam['exam_code'],
                    exam['title'],
                    exam['subject_name'],
                    f"{exam['duration']} phút",
                    exam['total_questions'],
                    created_date
                ), tags=(exam['id'],))
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách đề thi: {str(e)}")
    
    def create_exam(self):
        """Tạo đề thi mới"""
        exam_code = self.exam_code_var.get().strip()
        exam_title = self.exam_title_var.get().strip()
        subject_name = self.subject_var.get()
        question_count = self.question_count_var.get().strip()
        duration = self.duration_var.get().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not all([exam_code, exam_title, subject_name, question_count, duration]):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            question_count = int(question_count)
            duration = int(duration)
            
            if question_count <= 0 or duration <= 0:
                messagebox.showwarning("Cảnh báo", "Số câu hỏi và thời gian phải lớn hơn 0!")
                return
                
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số câu hỏi và thời gian phải là số!")
            return
        
        subject_id = self.subject_dict.get(subject_name)
        creator_id = self.auth_manager.get_current_user()['id']
        
        try:
            # Kiểm tra mã đề đã tồn tại chưa
            check_query = "SELECT id FROM exams WHERE exam_code = %s"
            existing = self.db.execute_query(check_query, (exam_code,))
            
            if existing:
                messagebox.showerror("Lỗi", "Mã đề đã tồn tại!")
                return
            
            # Kiểm tra số câu hỏi có sẵn
            count_query = "SELECT COUNT(*) as count FROM questions WHERE subject_id = %s"
            available_questions = self.db.execute_query(count_query, (subject_id,))
            
            if not available_questions or available_questions[0]['count'] < question_count:
                messagebox.showerror("Lỗi", f"Không đủ câu hỏi cho môn {subject_name}! "
                                         f"Cần {question_count} câu, có sẵn {available_questions[0]['count'] if available_questions else 0} câu.")
                return
            
            # Tạo đề thi
            insert_query = """
                INSERT INTO exams (exam_code, subject_id, title, duration, total_questions, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(insert_query, (
                exam_code, subject_id, exam_title, duration, question_count, creator_id
            ))
            
            exam_id = self.db.get_last_insert_id()
            
            # Chọn câu hỏi ngẫu nhiên
            questions_query = """
                SELECT id FROM questions 
                WHERE subject_id = %s 
                ORDER BY RAND() 
                LIMIT %s
            """
            questions = self.db.execute_query(questions_query, (subject_id, question_count))
            
            # Thêm câu hỏi vào đề thi
            exam_questions_query = """
                INSERT INTO exam_questions (exam_id, question_id, question_order)
                VALUES (%s, %s, %s)
            """
            
            for i, question in enumerate(questions):
                self.db.execute_query(exam_questions_query, (exam_id, question['id'], i + 1))
            
            messagebox.showinfo("Thành công", f"Đã tạo đề thi {exam_code} thành công!")
            
            # Xóa form
            self.exam_code_var.set("")
            self.exam_title_var.set("")
            self.question_count_var.set("20")
            self.duration_var.set("30")
            
            # Cập nhật danh sách
            self.load_exams()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo đề thi: {str(e)}")
    
    def view_exam_details(self):
        """Xem chi tiết đề thi"""
        selection = self.exams_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đề thi!")
            return
        
        exam_id = self.exams_tree.item(selection[0], "tags")[0]
        
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
            
            exam = exam_info[0]
            
            # Lấy danh sách câu hỏi
            query = """
                SELECT q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, 
                       q.correct_answer, eq.question_order
                FROM questions q
                JOIN exam_questions eq ON q.id = eq.question_id
                WHERE eq.exam_id = %s
                ORDER BY eq.question_order
            """
            questions = self.db.execute_query(query, (exam_id,))
            
            # Hiển thị dialog chi tiết
            self.show_exam_details_dialog(exam, questions)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xem chi tiết đề thi: {str(e)}")
    
    def show_exam_details_dialog(self, exam, questions):
        """Hiển thị dialog chi tiết đề thi"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Chi tiết đề thi: {exam['exam_code']}")
        dialog.geometry("700x500")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Frame chính
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Thông tin đề thi
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin đề thi", padding="10")
        info_frame.pack(fill="x", pady=(0, 10))
        
        info_text = f"""
        Mã đề: {exam['exam_code']}
        Tên đề: {exam['title']}
        Môn học: {exam['subject_name']}
        Thời gian: {exam['duration']} phút
        Số câu hỏi: {exam['total_questions']}
        Ngày tạo: {exam['created_at'].strftime('%d/%m/%Y %H:%M')}
        """
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor="w")
        
        # Frame câu hỏi
        questions_frame = ttk.LabelFrame(main_frame, text="Danh sách câu hỏi", padding="10")
        questions_frame.pack(fill="both", expand=True)
        
        # Text widget cho câu hỏi
        text_widget = tk.Text(questions_frame, wrap="word", state="disabled")
        text_widget.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(questions_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Hiển thị câu hỏi
        text_widget.config(state="normal")
        for i, question in enumerate(questions, 1):
            text_widget.insert(tk.END, f"Câu {i}: {question['question_text']}\n")
            text_widget.insert(tk.END, f"A. {question['option_a']}\n")
            text_widget.insert(tk.END, f"B. {question['option_b']}\n")
            text_widget.insert(tk.END, f"C. {question['option_c']}\n")
            text_widget.insert(tk.END, f"D. {question['option_d']}\n")
            text_widget.insert(tk.END, f"Đáp án đúng: {question['correct_answer']}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        text_widget.config(state="disabled")
    
    def delete_exam(self):
        """Xóa đề thi"""
        selection = self.exams_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đề thi!")
            return
        
        exam_id = self.exams_tree.item(selection[0], "tags")[0]
        exam_code = self.exams_tree.item(selection[0], "values")[0]
        
        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa đề thi {exam_code}?")
        
        if result:
            try:
                # Xóa câu hỏi trong đề thi
                delete_questions_query = "DELETE FROM exam_questions WHERE exam_id = %s"
                self.db.execute_query(delete_questions_query, (exam_id,))
                
                # Xóa đề thi
                delete_exam_query = "DELETE FROM exams WHERE id = %s"
                self.db.execute_query(delete_exam_query, (exam_id,))
                
                messagebox.showinfo("Thành công", f"Đã xóa đề thi {exam_code}!")
                self.load_exams()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa đề thi: {str(e)}")
    
    def logout(self):
        """Đăng xuất"""
        self.auth_manager.logout()
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 