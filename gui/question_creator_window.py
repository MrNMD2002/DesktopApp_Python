import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.database_manager import DatabaseManager
from utils.docx_reader import DocxReader

class QuestionCreatorWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db = DatabaseManager()
        self.docx_reader = DocxReader()
        self.setup_ui()
        self.load_subjects()
    
    def setup_ui(self):
        """Thiết lập giao diện người làm đề"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Người làm đề - Hệ thống Quản lý Đề thi")
        self.window.geometry("600x500")
        
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
        
        # Frame chọn môn học
        subject_frame = ttk.LabelFrame(main_frame, text="Chọn môn học", padding="10")
        subject_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(subject_frame, text="Môn học:").grid(row=0, column=0, sticky="w")
        
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(subject_frame, textvariable=self.subject_var, 
                                         state="readonly", width=30)
        self.subject_combo.grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # Frame upload file
        upload_frame = ttk.LabelFrame(main_frame, text="Upload file .docx", padding="10")
        upload_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(upload_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=0, sticky="ew")
        
        ttk.Button(upload_frame, text="Chọn file", 
                  command=self.select_file).grid(row=0, column=1, padx=(10, 0))
        
        ttk.Button(upload_frame, text="Đọc file", 
                  command=self.read_file).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Frame hướng dẫn
        guide_frame = ttk.LabelFrame(main_frame, text="Hướng dẫn định dạng", padding="10")
        guide_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        guide_text = self.docx_reader.get_template_instructions()
        guide_label = ttk.Label(guide_frame, text=guide_text, justify=tk.LEFT)
        guide_label.grid(row=0, column=0, sticky="w")
        
        # Frame thống kê
        stats_frame = ttk.LabelFrame(main_frame, text="Thống kê câu hỏi", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        # Treeview cho thống kê
        columns = ("Môn học", "Tổng câu hỏi", "Dễ", "Trung bình", "Khó")
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100)
        
        self.stats_tree.grid(row=0, column=0, sticky="ew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        # Nút refresh thống kê
        ttk.Button(stats_frame, text="Làm mới thống kê", 
                  command=self.load_statistics).grid(row=1, column=0, pady=10)
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        upload_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)
    
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
    
    def select_file(self):
        """Chọn file .docx"""
        file_path = filedialog.askopenfilename(
            title="Chọn file .docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
    
    def read_file(self):
        """Đọc file .docx và import câu hỏi"""
        file_path = self.file_path_var.get().strip()
        subject_name = self.subject_var.get()
        
        if not file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file!")
            return
        
        if not subject_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học!")
            return
        
        subject_id = self.subject_dict.get(subject_name)
        creator_id = self.auth_manager.get_current_user()['id']
        
        try:
            # Hiển thị dialog xác nhận
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có muốn import câu hỏi từ file này vào môn {subject_name}?")
            
            if result:
                # Đọc file
                success, message = self.docx_reader.read_docx_file(file_path, subject_id, creator_id)
                
                if success:
                    messagebox.showinfo("Thành công", message)
                    self.file_path_var.set("")  # Xóa đường dẫn file
                    self.load_statistics()  # Cập nhật thống kê
                else:
                    messagebox.showerror("Lỗi", message)
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def load_statistics(self):
        """Tải thống kê câu hỏi"""
        try:
            query = """
                SELECT s.name as subject_name,
                       COUNT(q.id) as total_questions,
                       SUM(CASE WHEN q.difficulty_level = 'easy' THEN 1 ELSE 0 END) as easy_count,
                       SUM(CASE WHEN q.difficulty_level = 'medium' THEN 1 ELSE 0 END) as medium_count,
                       SUM(CASE WHEN q.difficulty_level = 'hard' THEN 1 ELSE 0 END) as hard_count
                FROM subjects s
                LEFT JOIN questions q ON s.id = q.subject_id
                GROUP BY s.id, s.name
                ORDER BY s.name
            """
            
            stats = self.db.execute_query(query)
            
            # Xóa dữ liệu cũ
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            # Thêm dữ liệu mới
            for stat in stats:
                self.stats_tree.insert("", "end", values=(
                    stat['subject_name'],
                    stat['total_questions'] or 0,
                    stat['easy_count'] or 0,
                    stat['medium_count'] or 0,
                    stat['hard_count'] or 0
                ))
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thống kê: {str(e)}")
    
    def logout(self):
        """Đăng xuất"""
        self.auth_manager.logout()
        self.window.destroy()
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 