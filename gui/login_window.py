import tkinter as tk
from tkinter import ttk, messagebox
from utils.auth import AuthManager
from gui.password_window import ForgotPasswordWindow

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.auth_manager = AuthManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện đăng nhập"""
        # Tạo cửa sổ đăng nhập
        self.login_window = tk.Toplevel(self.parent)
        self.login_window.title("Đăng nhập - Hệ thống Quản lý Đề thi")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.login_window.transient(self.parent)
        self.login_window.grab_set()
        
        # Frame chính
        main_frame = ttk.Frame(self.login_window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="ĐĂNG NHẬP HỆ THỐNG", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Tên đăng nhập
        ttk.Label(main_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Mật khẩu
        ttk.Label(main_frame, text="Mật khẩu:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                       show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Vai trò
        ttk.Label(main_frame, text="Vai trò:").grid(row=3, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=27)
        role_combo.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Frame nút bấm
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Nút đăng nhập
        login_button = ttk.Button(button_frame, text="Đăng nhập", 
                                 command=self.login, style="Accent.TButton")
        login_button.grid(row=0, column=0, padx=(0, 10))
        
        # Nút quên mật khẩu
        forgot_button = ttk.Button(button_frame, text="Quên mật khẩu", 
                                  command=self.show_forgot_password)
        forgot_button.grid(row=0, column=1)
        
        # Thông tin tài khoản mẫu
        info_frame = ttk.LabelFrame(main_frame, text="Tài khoản mẫu", padding="10")
        info_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        info_text = """
        Tài khoản mẫu (mật khẩu: 123456):
        - student1 (Học sinh)
        - creator1 (Người làm đề)
        - admin (Người sinh đề)
        """
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus vào username entry
        self.username_entry.focus()
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()         
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Thực hiện đăng nhập
        success, message = self.auth_manager.login(username, password)
        
        if success:
            # Kiểm tra vai trò
            if self.auth_manager.has_role(role):
                messagebox.showinfo("Thành công", message)
                self.login_window.destroy()
                self.open_main_window(role)
            else:
                messagebox.showerror("Lỗi", f"Tài khoản không có quyền truy cập với vai trò {role}")
                self.auth_manager.logout()
        else:
            messagebox.showerror("Lỗi", message)
    
    def show_forgot_password(self):
        """Hiển thị cửa sổ quên mật khẩu"""
        ForgotPasswordWindow(self.login_window, self.auth_manager)
    
    def open_main_window(self, role):
        """Mở cửa sổ chính theo vai trò"""
        if role == "student":
            from gui.student_window import StudentWindow
            StudentWindow(self.parent, self.auth_manager)
        elif role == "question_creator":
            from gui.question_creator_window import QuestionCreatorWindow
            QuestionCreatorWindow(self.parent, self.auth_manager)
        elif role == "exam_generator" or role == "admin":
            from gui.exam_generator_window import ExamGeneratorWindow
            ExamGeneratorWindow(self.parent, self.auth_manager) 