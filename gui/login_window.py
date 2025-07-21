import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service
from gui.styles import ModernStyles

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent  # parent là instance của ExamBankApp
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("🔐 Đăng nhập - Hệ thống Quản lý Ngân hàng Đề thi")
        self.window.geometry("450x350")
        self.window.resizable(False, False)
        
        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.window.configure(bg=ModernStyles.COLORS['light'])
        
        # Center window
        ModernStyles.center_window(self.window, 450, 350)
        
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ModernStyles.create_modern_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title section
        title_frame = ModernStyles.create_modern_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 30))
        
        title = ModernStyles.create_title_label(title_frame, "🔐 ĐĂNG NHẬP")
        title.pack()
        
        subtitle = ModernStyles.create_subtitle_label(title_frame, "Hệ thống Quản lý Ngân hàng Đề thi")
        subtitle.pack(pady=(5, 0))
        
        # Login form
        form_frame = ModernStyles.create_modern_frame(main_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Username field
        username_frame = ModernStyles.create_modern_frame(form_frame)
        username_frame.pack(fill="x", pady=(0, 15))
        
        username_label = ModernStyles.create_modern_label(username_frame, "👤 Tên đăng nhập:")
        username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_entry = ModernStyles.create_modern_entry(username_frame, 
                                                              textvariable=self.username_var,
                                                              width=35)
        self.username_entry.pack(fill="x")
        
        # Password field
        password_frame = ModernStyles.create_modern_frame(form_frame)
        password_frame.pack(fill="x", pady=(0, 25))
        
        password_label = ModernStyles.create_modern_label(password_frame, "🔒 Mật khẩu:")
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ModernStyles.create_modern_entry(password_frame, 
                                                              textvariable=self.password_var,
                                                              show="*",
                                                              width=35)
        self.password_entry.pack(fill="x")
        
        # Buttons section
        button_frame = ModernStyles.create_modern_frame(main_frame)
        button_frame.pack(fill="x")
        
        self.login_btn = ModernStyles.create_success_button(button_frame, 
                                                           "🚀 Đăng nhập", 
                                                           command=self.login)
        self.login_btn.pack(pady=(0, 10))
        
        # Info section
        info_frame = ModernStyles.create_modern_frame(main_frame)
        info_frame.pack(fill="x", pady=(20, 0))
        
        info_label = ModernStyles.create_info_label(info_frame, 
                                                   "💡 Nhấn Enter để đăng nhập nhanh")
        info_label.pack()
        
        # Bind events
        self.window.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        try:
            user = user_service.login(username, password)
            self.parent.current_user = user
            messagebox.showinfo("Thành công", f"Đăng nhập thành công! Xin chào {user['full_name']}")
            self.window.withdraw()  # Ẩn cửa sổ đăng nhập thay vì đóng
            self.parent.show_main_window_after_login()
        except Exception as e:
            messagebox.showerror("Lỗi đăng nhập", str(e))