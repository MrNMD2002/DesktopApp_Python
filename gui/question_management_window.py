import tkinter as tk
from tkinter import ttk, messagebox
from utils.question_manager import QuestionManager
from utils.auth import AuthManager
import json
import logging
import re

class QuestionManagementWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.question_manager = QuestionManager()
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_subjects()
        self.load_questions()
        self.selected_question_id = None
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Quản lý Câu hỏi")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Style
        style = ttk.Style()
        style.configure('Success.TButton', background='#28a745', foreground='white')
        style.configure('Danger.TButton', background='#dc3545', foreground='white')
        style.configure('Warning.TButton', background='#ffc107', foreground='black')
        style.configure('Info.TButton', background='#17a2b8', foreground='white')
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Notebook để tạo tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab quản lý câu hỏi
        self.questions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.questions_frame, text="Quản lý Câu hỏi")
        self.create_questions_tab()
        
        # Tab lịch sử (chỉ admin và giáo viên)
        if self.auth_manager.is_admin() or self.auth_manager.has_role('question_creator'):
            self.history_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.history_frame, text="Lịch sử Chỉnh sửa")
            self.create_history_tab()
        
        # Tab thống kê
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Thống kê")
        self.create_stats_tab()
    
    def create_questions_tab(self):
        """Tạo tab quản lý câu hỏi"""
        # Frame chính
        main_frame = ttk.Frame(self.questions_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.questions_frame.columnconfigure(0, weight=1)
        self.questions_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="QUẢN LÝ CÂU HỎI", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame bên trái - Form thêm/sửa câu hỏi
        form_frame = ttk.LabelFrame(main_frame, text="Thông tin câu hỏi", padding="10")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Môn học
        ttk.Label(form_frame, text="Môn học:").grid(row=0, column=0, sticky="w", pady=2)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(form_frame, textvariable=self.subject_var, 
                                         state="readonly", width=20)
        self.subject_combo.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Độ khó
        ttk.Label(form_frame, text="Độ khó:").grid(row=1, column=0, sticky="w", pady=2)
        self.difficulty_var = tk.StringVar(value="medium")
        difficulty_combo = ttk.Combobox(form_frame, textvariable=self.difficulty_var,
                                       values=["easy", "medium", "hard"], state="readonly", width=20)
        difficulty_combo.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Câu hỏi
        ttk.Label(form_frame, text="Câu hỏi:").grid(row=2, column=0, sticky="w", pady=2)
        self.question_text = tk.Text(form_frame, height=4, width=30)
        self.question_text.grid(row=2, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Đáp án A
        ttk.Label(form_frame, text="Đáp án A:").grid(row=3, column=0, sticky="w", pady=2)
        self.option_a_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.option_a_var, width=30).grid(row=3, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Đáp án B
        ttk.Label(form_frame, text="Đáp án B:").grid(row=4, column=0, sticky="w", pady=2)
        self.option_b_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.option_b_var, width=30).grid(row=4, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Đáp án C
        ttk.Label(form_frame, text="Đáp án C:").grid(row=5, column=0, sticky="w", pady=2)
        self.option_c_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.option_c_var, width=30).grid(row=5, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Đáp án D
        ttk.Label(form_frame, text="Đáp án D:").grid(row=6, column=0, sticky="w", pady=2)
        self.option_d_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.option_d_var, width=30).grid(row=6, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Đáp án đúng
        ttk.Label(form_frame, text="Đáp án đúng:").grid(row=7, column=0, sticky="w", pady=2)
        self.correct_answer_var = tk.StringVar()
        correct_combo = ttk.Combobox(form_frame, textvariable=self.correct_answer_var,
                                    values=["A", "B", "C", "D"], state="readonly", width=20)
        correct_combo.grid(row=7, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Cấu hình grid cho form_frame
        form_frame.columnconfigure(1, weight=1)
        
        # Frame nút bấm
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(20, 0))
        
        self.add_button = ttk.Button(button_frame, text="Thêm mới", 
                                    command=self.add_question, style="Success.TButton")
        self.add_button.grid(row=0, column=0, padx=(0, 5))
        
        self.update_button = ttk.Button(button_frame, text="Cập nhật", 
                                       command=self.update_question, style="Warning.TButton")
        self.update_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Xóa form", 
                                      command=self.clear_form)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        # Frame bên phải - Bảng danh sách câu hỏi
        list_frame = ttk.LabelFrame(main_frame, text="Danh sách câu hỏi", padding="10")
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Frame filter
        filter_frame = ttk.Frame(list_frame)
        filter_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Lọc theo:").pack(side=tk.LEFT)
        
        self.filter_subject_var = tk.StringVar(value="Tất cả")
        self.filter_subject_combo = ttk.Combobox(filter_frame, textvariable=self.filter_subject_var,
                                           state="readonly", width=15)
        self.filter_subject_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        self.filter_difficulty_var = tk.StringVar(value="Tất cả")
        filter_difficulty_combo = ttk.Combobox(filter_frame, textvariable=self.filter_difficulty_var,
                                              values=["Tất cả", "easy", "medium", "hard"], state="readonly", width=10)
        filter_difficulty_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(filter_frame, text="Lọc", command=self.filter_questions).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="Làm mới", command=self.load_questions).pack(side=tk.LEFT)
        
        # Tạo Treeview
        columns = ("ID", "Môn học", "Câu hỏi", "Đáp án", "Độ khó", "Trạng thái", "Người tạo", "Ngày tạo")
        self.questions_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình cột
        self.questions_tree.heading("ID", text="ID")
        self.questions_tree.heading("Môn học", text="Môn học")
        self.questions_tree.heading("Câu hỏi", text="Câu hỏi")
        self.questions_tree.heading("Đáp án", text="Đáp án")
        self.questions_tree.heading("Độ khó", text="Độ khó")
        self.questions_tree.heading("Trạng thái", text="Trạng thái")
        self.questions_tree.heading("Người tạo", text="Người tạo")
        self.questions_tree.heading("Ngày tạo", text="Ngày tạo")
        
        # Độ rộng cột
        self.questions_tree.column("ID", width=50)
        self.questions_tree.column("Môn học", width=100)
        self.questions_tree.column("Câu hỏi", width=200)
        self.questions_tree.column("Đáp án", width=50)
        self.questions_tree.column("Độ khó", width=80)
        self.questions_tree.column("Trạng thái", width=80)
        self.questions_tree.column("Người tạo", width=100)
        self.questions_tree.column("Ngày tạo", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.questions_tree.yview)
        self.questions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.questions_tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Cấu hình grid cho list_frame
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Frame nút bấm cho danh sách
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.detail_button = ttk.Button(list_button_frame, text="Xem chi tiết", 
                                       command=self.show_question_detail, style="Info.TButton")
        self.detail_button.grid(row=0, column=0, padx=(0, 5))
        
        self.delete_button = ttk.Button(list_button_frame, text="Xóa", 
                                       command=self.delete_question, style="Danger.TButton")
        self.delete_button.grid(row=0, column=1, padx=5)
        
        self.restore_button = ttk.Button(list_button_frame, text="Khôi phục", 
                                        command=self.restore_question, style="Info.TButton")
        self.restore_button.grid(row=0, column=2, padx=5)
        
        self.history_button = ttk.Button(list_button_frame, text="Xem lịch sử", 
                                        command=self.show_question_history)
        self.history_button.grid(row=0, column=3, padx=5)
        
        # Bind events
        self.questions_tree.bind("<<TreeviewSelect>>", self.on_question_select)
    
    def create_history_tab(self):
        """Tạo tab lịch sử chỉnh sửa"""
        # Frame chính
        main_frame = ttk.Frame(self.history_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="LỊCH SỬ CHỈNH SỬA CÂU HỎI", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Tạo Treeview cho lịch sử
        columns = ("Thời gian", "Câu hỏi", "Hành động", "Người thực hiện", "Môn học")
        self.history_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        # Cấu hình cột
        self.history_tree.heading("Thời gian", text="Thời gian")
        self.history_tree.heading("Câu hỏi", text="Câu hỏi")
        self.history_tree.heading("Hành động", text="Hành động")
        self.history_tree.heading("Người thực hiện", text="Người thực hiện")
        self.history_tree.heading("Môn học", text="Môn học")
        
        # Độ rộng cột
        self.history_tree.column("Thời gian", width=150)
        self.history_tree.column("Câu hỏi", width=300)
        self.history_tree.column("Hành động", width=100)
        self.history_tree.column("Người thực hiện", width=150)
        self.history_tree.column("Môn học", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.history_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Nút làm mới
        ttk.Button(main_frame, text="Làm mới", command=self.load_history).pack(pady=10)
        
        # Bind double click để xem chi tiết
        self.history_tree.bind("<Double-1>", self.show_history_detail)
    
    def create_stats_tab(self):
        """Tạo tab thống kê"""
        # Frame chính
        main_frame = ttk.Frame(self.stats_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="THỐNG KÊ CÂU HỎI", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Tạo Treeview cho thống kê
        columns = ("Môn học", "Hoạt động", "Đã xóa", "Dễ", "Trung bình", "Khó", "Tổng cộng")
        self.stats_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        # Cấu hình cột
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.stats_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Nút làm mới
        ttk.Button(main_frame, text="Làm mới", command=self.load_statistics).pack(pady=10)
    
    def load_subjects(self):
        """Tải danh sách môn học"""
        try:
            query = "SELECT id, name FROM subjects ORDER BY name"
            subjects = self.question_manager.db.execute_query(query)
            
            subject_dict = {}
            subject_names = ["Tất cả"]
            
            for subject in subjects:
                subject_dict[subject['name']] = subject['id']
                subject_names.append(subject['name'])
            
            self.subject_combo['values'] = subject_names[1:]  # Bỏ "Tất cả"
            self.filter_subject_combo['values'] = subject_names
            self.subject_dict = subject_dict
            
            if len(subject_names) > 1:
                self.subject_combo.set(subject_names[1])
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")
    
    def load_questions(self, subject_id=None, difficulty=None):
        """Tải danh sách câu hỏi"""
        try:
            # Xóa dữ liệu cũ
            for item in self.questions_tree.get_children():
                self.questions_tree.delete(item)
            
            # Lấy danh sách câu hỏi
            questions = self.question_manager.get_all_questions(subject_id, difficulty)
            
            for question in questions:
                # Format dữ liệu
                status = "Hoạt động" if question['is_active'] else "Đã xóa"
                created_date = question['created_at'].strftime('%d/%m/%Y') if question['created_at'] else ""
                
                # Cắt ngắn câu hỏi nếu quá dài
                question_text = question['question_text']
                if len(question_text) > 50:
                    question_text = question_text[:50] + "..."
                
                self.questions_tree.insert("", "end", values=(
                    question['id'],
                    question['subject_name'],
                    question_text,
                    question['correct_answer'],
                    question['difficulty_level'],
                    status,
                    question['created_by_name'],
                    created_date
                ), tags=(question['id'],))
            
            logging.info(f"Đã tải {len(questions)} câu hỏi")
        except Exception as e:
            logging.error(f"Lỗi tải danh sách câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải danh sách câu hỏi: {str(e)}")
    
    def filter_questions(self):
        """Lọc câu hỏi"""
        subject_name = self.filter_subject_var.get()
        difficulty = self.filter_difficulty_var.get()
        
        subject_id = None
        if subject_name != "Tất cả":
            subject_id = self.subject_dict.get(subject_name)
        
        if difficulty == "Tất cả":
            difficulty = None
        
        self.load_questions(subject_id, difficulty)
    
    def clear_form(self):
        """Xóa form"""
        self.subject_var.set("")
        self.difficulty_var.set("medium")
        self.question_text.delete(1.0, tk.END)
        self.option_a_var.set("")
        self.option_b_var.set("")
        self.option_c_var.set("")
        self.option_d_var.set("")
        self.correct_answer_var.set("")
        self.selected_question_id = None
        
        # Cập nhật trạng thái nút
        self.add_button.config(state="normal")
        self.update_button.config(state="disabled")
    
    def show_question_detail(self):
        """Hiển thị chi tiết câu hỏi với thông tin bổ sung"""
        if not self.selected_question_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi để xem chi tiết")
            return
        
        try:
            # Lấy thông tin chi tiết câu hỏi
            question = self.question_manager.get_question_by_id(self.selected_question_id)
            if not question:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin câu hỏi")
                return
            
            # Tạo dialog hiển thị chi tiết
            dialog = tk.Toplevel(self.window)
            dialog.title(f"Chi tiết câu hỏi #{question['id']}")
            dialog.geometry("600x500")
            dialog.transient(self.window)
            dialog.grab_set()
            
            # Frame chính
            main_frame = ttk.Frame(dialog, padding="10")
            main_frame.pack(fill="both", expand=True)
            
            # Tiêu đề
            title_label = ttk.Label(main_frame, text=f"CHI TIẾT CÂU HỎI #{question['id']}", 
                                   font=("Arial", 14, "bold"))
            title_label.pack(pady=(0, 20))
            
            # Frame thông tin cơ bản
            info_frame = ttk.LabelFrame(main_frame, text="Thông tin cơ bản", padding="10")
            info_frame.pack(fill="x", pady=(0, 10))
            
            info_text = f"""
            Môn học: {question['subject_name']}
            Độ khó: {question['difficulty_level']}
            Đáp án đúng: {question['correct_answer']}
            Người tạo: {question['created_by_name']}
            Ngày tạo: {question['created_at'].strftime('%d/%m/%Y %H:%M') if question['created_at'] else 'N/A'}
            Trạng thái: {'Hoạt động' if question['is_active'] else 'Đã xóa'}
            """
            
            ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor="w")
            
            # Frame câu hỏi
            question_frame = ttk.LabelFrame(main_frame, text="Nội dung câu hỏi", padding="10")
            question_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Text widget cho câu hỏi
            question_text = tk.Text(question_frame, wrap="word", height=8, state="disabled")
            question_text.pack(fill="both", expand=True)
            
            # Scrollbar cho câu hỏi
            question_scrollbar = ttk.Scrollbar(question_frame, orient="vertical", command=question_text.yview)
            question_scrollbar.pack(side="right", fill="y")
            question_text.configure(yscrollcommand=question_scrollbar.set)
            
            # Hiển thị câu hỏi với thông tin bổ sung
            question_text.config(state="normal")
            question_text.delete(1.0, tk.END)
            
            # Phân tích thông tin bổ sung từ question_text
            full_text = question['question_text']
            additional_info = []
            
            # Tìm thông tin bổ sung trong dấu ngoặc vuông
            info_match = re.search(r'\[(.*?)\]$', full_text, re.MULTILINE)
            if info_match:
                info_text = info_match.group(1)
                additional_info = [item.strip() for item in info_text.split('|')]
                # Loại bỏ phần thông tin bổ sung khỏi câu hỏi chính
                full_text = re.sub(r'\[.*?\]$', '', full_text, flags=re.MULTILINE).strip()
            
            # Hiển thị câu hỏi chính
            question_text.insert(tk.END, f"Câu hỏi:\n{full_text}\n\n")
            
            # Hiển thị thông tin bổ sung nếu có
            if additional_info:
                question_text.insert(tk.END, "📋 Thông tin bổ sung:\n")
                for info in additional_info:
                    question_text.insert(tk.END, f"• {info}\n")
            
            question_text.config(state="disabled")
            
            # Frame đáp án
            options_frame = ttk.LabelFrame(main_frame, text="Các đáp án", padding="10")
            options_frame.pack(fill="x", pady=(0, 10))
            
            options_text = f"""
            A. {question['option_a']}
            B. {question['option_b']}
            C. {question['option_c']}
            D. {question['option_d']}
            """
            
            ttk.Label(options_frame, text=options_text, justify=tk.LEFT).pack(anchor="w")
            
            # Nút đóng
            ttk.Button(main_frame, text="Đóng", command=dialog.destroy).pack(pady=10)
            
        except Exception as e:
            logging.error(f"Lỗi hiển thị chi tiết câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể hiển thị chi tiết câu hỏi: {str(e)}")
    
    def on_question_select(self, event):
        """Xử lý khi chọn câu hỏi trong bảng"""
        selection = self.questions_tree.selection()
        if selection:
            item = self.questions_tree.item(selection[0])
            values = item['values']
            
            # Lưu ID câu hỏi đang chọn
            self.selected_question_id = values[0]
            
            # Lấy thông tin chi tiết câu hỏi
            question = self.question_manager.get_question_by_id(self.selected_question_id)
            if question:
                # Điền thông tin vào form
                self.subject_var.set(question['subject_name'])
                self.difficulty_var.set(question['difficulty_level'])
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, question['question_text'])
                self.option_a_var.set(question['option_a'])
                self.option_b_var.set(question['option_b'])
                self.option_c_var.set(question['option_c'])
                self.option_d_var.set(question['option_d'])
                self.correct_answer_var.set(question['correct_answer'])
                
                # Cập nhật trạng thái nút
                self.add_button.config(state="disabled")
                self.update_button.config(state="normal")
    
    def add_question(self):
        """Thêm câu hỏi mới"""
        try:
            # Lấy dữ liệu từ form
            subject_name = self.subject_var.get()
            difficulty = self.difficulty_var.get()
            question_text = self.question_text.get(1.0, tk.END).strip()
            option_a = self.option_a_var.get().strip()
            option_b = self.option_b_var.get().strip()
            option_c = self.option_c_var.get().strip()
            option_d = self.option_d_var.get().strip()
            correct_answer = self.correct_answer_var.get()
            
            # Kiểm tra dữ liệu
            if not all([subject_name, question_text, option_a, option_b, option_c, option_d, correct_answer]):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
                return
            
            subject_id = self.subject_dict.get(subject_name)
            if not subject_id:
                messagebox.showerror("Lỗi", "Môn học không hợp lệ")
                return
            
            current_user = self.auth_manager.get_current_user()
            
            # Tạo câu hỏi
            success, message = self.question_manager.create_question(
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_answer, difficulty, current_user['id']
            )
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_questions()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi thêm câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm câu hỏi: {str(e)}")
    
    def update_question(self):
        """Cập nhật câu hỏi"""
        if not self.selected_question_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi cần cập nhật")
            return
        
        try:
            # Lấy dữ liệu từ form
            subject_name = self.subject_var.get()
            difficulty = self.difficulty_var.get()
            question_text = self.question_text.get(1.0, tk.END).strip()
            option_a = self.option_a_var.get().strip()
            option_b = self.option_b_var.get().strip()
            option_c = self.option_c_var.get().strip()
            option_d = self.option_d_var.get().strip()
            correct_answer = self.correct_answer_var.get()
            
            # Kiểm tra dữ liệu
            if not all([subject_name, question_text, option_a, option_b, option_c, option_d, correct_answer]):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
                return
            
            subject_id = self.subject_dict.get(subject_name)
            if not subject_id:
                messagebox.showerror("Lỗi", "Môn học không hợp lệ")
                return
            
            current_user = self.auth_manager.get_current_user()
            
            # Cập nhật câu hỏi
            success, message = self.question_manager.update_question(
                self.selected_question_id, subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_answer, difficulty, current_user['id']
            )
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_questions()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi cập nhật câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật câu hỏi: {str(e)}")
    
    def delete_question(self):
        """Xóa câu hỏi"""
        selection = self.questions_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi cần xóa")
            return
        
        item = self.questions_tree.item(selection[0])
        question_id = item['values'][0]
        question_text = item['values'][2]
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", 
                                     f"Bạn có chắc chắn muốn xóa câu hỏi này?\n\n{question_text}")
        if not confirm:
            return
        
        try:
            current_user = self.auth_manager.get_current_user()
            success, message = self.question_manager.delete_question(question_id, current_user['id'])
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_questions()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi xóa câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể xóa câu hỏi: {str(e)}")
    
    def restore_question(self):
        """Khôi phục câu hỏi"""
        selection = self.questions_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi cần khôi phục")
            return
        
        item = self.questions_tree.item(selection[0])
        question_id = item['values'][0]
        status = item['values'][5]
        
        if status == "Hoạt động":
            messagebox.showinfo("Thông báo", "Câu hỏi này chưa bị xóa")
            return
        
        try:
            current_user = self.auth_manager.get_current_user()
            success, message = self.question_manager.restore_question(question_id, current_user['id'])
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.load_questions()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi khôi phục câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể khôi phục câu hỏi: {str(e)}")
    
    def show_question_history(self):
        """Hiển thị lịch sử câu hỏi"""
        if not self.selected_question_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi để xem lịch sử")
            return
        
        QuestionHistoryWindow(self.window, self.question_manager, self.selected_question_id)
    
    def load_history(self):
        """Tải lịch sử chỉnh sửa"""
        try:
            # Xóa dữ liệu cũ
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Lấy lịch sử
            if self.auth_manager.is_admin():
                history = self.question_manager.get_all_question_history()
            else:
                # Giáo viên chỉ xem lịch sử câu hỏi mình tạo
                current_user = self.auth_manager.get_current_user()
                history = self.question_manager.get_question_history_by_user(current_user['id'])
            
            for record in history:
                # Format dữ liệu
                changed_date = record['changed_at'].strftime('%d/%m/%Y %H:%M') if record['changed_at'] else ""
                
                # Cắt ngắn câu hỏi nếu quá dài
                question_text = record.get('question_text', '')
                if len(question_text) > 50:
                    question_text = question_text[:50] + "..."
                
                # Dịch hành động
                action_map = {
                    'created': 'Tạo mới',
                    'updated': 'Cập nhật',
                    'deleted': 'Xóa',
                    'restored': 'Khôi phục'
                }
                action = action_map.get(record['action'], record['action'])
                
                self.history_tree.insert("", "end", values=(
                    changed_date,
                    question_text,
                    action,
                    record['changed_by_name'],
                    record.get('subject_name', '')
                ), tags=(record['id'],))
            
        except Exception as e:
            logging.error(f"Lỗi tải lịch sử: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải lịch sử: {str(e)}")
    
    def show_history_detail(self, event):
        """Hiển thị chi tiết lịch sử"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']
            
            # Hiển thị dialog chi tiết
            HistoryDetailWindow(self.window, values)
    
    def load_statistics(self):
        """Tải thống kê"""
        try:
            # Xóa dữ liệu cũ
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            # Lấy thống kê
            stats = self.question_manager.get_question_statistics()
            
            for stat in stats:
                total = (stat['active_count'] or 0) + (stat['deleted_count'] or 0)
                
                self.stats_tree.insert("", "end", values=(
                    stat['subject_name'],
                    stat['active_count'] or 0,
                    stat['deleted_count'] or 0,
                    stat['easy_count'] or 0,
                    stat['medium_count'] or 0,
                    stat['hard_count'] or 0,
                    total
                ))
            
        except Exception as e:
            logging.error(f"Lỗi tải thống kê: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải thống kê: {str(e)}")


class QuestionHistoryWindow:
    def __init__(self, parent, question_manager, question_id):
        self.parent = parent
        self.question_manager = question_manager
        self.question_id = question_id
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_history()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Lịch sử Câu hỏi")
        self.window.geometry("800x500")
        self.window.resizable(True, True)
        
        # Căn giữa cửa sổ
        self.center_window()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="LỊCH SỬ CHỈNH SỬA CÂU HỎI", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Tạo Treeview
        columns = ("Thời gian", "Hành động", "Người thực hiện", "Chi tiết")
        self.history_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình cột
        self.history_tree.heading("Thời gian", text="Thời gian")
        self.history_tree.heading("Hành động", text="Hành động")
        self.history_tree.heading("Người thực hiện", text="Người thực hiện")
        self.history_tree.heading("Chi tiết", text="Chi tiết")
        
        # Độ rộng cột
        self.history_tree.column("Thời gian", width=150)
        self.history_tree.column("Hành động", width=100)
        self.history_tree.column("Người thực hiện", width=150)
        self.history_tree.column("Chi tiết", width=350)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.history_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Nút đóng
        ttk.Button(main_frame, text="Đóng", command=self.window.destroy).pack(pady=10)
        
        # Bind double click để xem chi tiết
        self.history_tree.bind("<Double-1>", self.show_detail)
    
    def load_history(self):
        """Tải lịch sử câu hỏi"""
        try:
            # Xóa dữ liệu cũ
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Lấy lịch sử
            history = self.question_manager.get_question_history(self.question_id)
            
            for record in history:
                # Format dữ liệu
                changed_date = record['changed_at'].strftime('%d/%m/%Y %H:%M') if record['changed_at'] else ""
                
                # Dịch hành động
                action_map = {
                    'created': 'Tạo mới',
                    'updated': 'Cập nhật',
                    'deleted': 'Xóa',
                    'restored': 'Khôi phục'
                }
                action = action_map.get(record['action'], record['action'])
                
                # Tạo chi tiết
                detail = self._create_detail_text(record)
                
                self.history_tree.insert("", "end", values=(
                    changed_date,
                    action,
                    record['changed_by_name'],
                    detail
                ), tags=(record['id'],))
            
        except Exception as e:
            logging.error(f"Lỗi tải lịch sử câu hỏi: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải lịch sử: {str(e)}")
    
    def _create_detail_text(self, record):
        """Tạo text chi tiết cho lịch sử"""
        try:
            if record['action'] == 'created':
                new_data = json.loads(record['new_data']) if record['new_data'] else {}
                return f"Tạo câu hỏi: {new_data.get('question_text', '')[:50]}..."
            
            elif record['action'] == 'updated':
                old_data = json.loads(record['old_data']) if record['old_data'] else {}
                new_data = json.loads(record['new_data']) if record['new_data'] else {}
                
                changes = []
                for key in ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'difficulty_level']:
                    if old_data.get(key) != new_data.get(key):
                        changes.append(f"{key}: {old_data.get(key, '')} → {new_data.get(key, '')}")
                
                return f"Cập nhật: {', '.join(changes[:2])}..." if changes else "Không có thay đổi"
            
            elif record['action'] == 'deleted':
                old_data = json.loads(record['old_data']) if record['old_data'] else {}
                return f"Xóa câu hỏi: {old_data.get('question_text', '')[:50]}..."
            
            elif record['action'] == 'restored':
                new_data = json.loads(record['new_data']) if record['new_data'] else {}
                return f"Khôi phục câu hỏi: {new_data.get('question_text', '')[:50]}..."
            
            return "Không có thông tin"
        except Exception as e:
            return "Lỗi hiển thị chi tiết"
    
    def show_detail(self, event):
        """Hiển thị chi tiết lịch sử"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']
            
            # Hiển thị dialog chi tiết
            HistoryDetailWindow(self.window, values)


class HistoryDetailWindow:
    def __init__(self, parent, history_data):
        self.parent = parent
        self.history_data = history_data
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Chi tiết Lịch sử")
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Căn giữa cửa sổ
        self.center_window()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="CHI TIẾT LỊCH SỬ", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Thông tin cơ bản
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin", padding="10")
        info_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Thời gian: {self.history_data[0]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Hành động: {self.history_data[1]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Người thực hiện: {self.history_data[2]}").pack(anchor="w")
        
        # Chi tiết
        detail_frame = ttk.LabelFrame(main_frame, text="Chi tiết", padding="10")
        detail_frame.pack(fill="both", expand=True)
        
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD)
        self.detail_text.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.detail_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Nút đóng
        ttk.Button(main_frame, text="Đóng", command=self.window.destroy).pack(pady=10)
        
        # Hiển thị chi tiết
        self.detail_text.insert(1.0, self.history_data[3])
        self.detail_text.config(state="disabled") 